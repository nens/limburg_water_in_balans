import os
from pathlib import Path
import requests
from typing import Union

from threedi_api_client.api import ThreediApi
from threedi_api_client.openapi import (
    Download
)
from threedi_api_client.openapi.exceptions import ApiException

from constants import THREEDI_API_HOST
from login import get_login_details
from exceptions import SchematisationHasNoRevisionsError

CHUNK_SIZE = 1024 ** 2

CONFIG = {
    "THREEDI_API_HOST": THREEDI_API_HOST,
    "THREEDI_API_USERNAME": get_login_details(option='username'),
    "THREEDI_API_PASSWORD": get_login_details(option='password')
}
THREEDI_API = ThreediApi(config=CONFIG, version='v3-beta')


def get_download_file(download, file_path):
    """Getting file from Download object and writing it under given path."""
    r = requests.get(download.get_url, stream=True, timeout=15)
    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)


def download_schematisation_revision_raster(
        raster_pk: int, schematisation_pk: int, revision_pk: int
) -> Download:
    """Download schematisation revision raster."""
    raster_download = THREEDI_API.schematisations_revisions_rasters_download(
        raster_pk, revision_pk, schematisation_pk
    )
    return raster_download


def download_latest_revision(schematisation_pk, target_directory: Union[Path, str]):
    target_directory = Path(target_directory)

    schematisation = THREEDI_API.schematisations_read(id=schematisation_pk)
    storage_dir = target_directory / schematisation.name
    os.makedirs(storage_dir, exist_ok=True)
    try:
        revision = THREEDI_API.schematisations_latest_revision(id=schematisation_pk)
    except ApiException as e:
        e_msg = str(e)
        try:
            reason = e_msg.split("\n")[3].split(":")[2].strip("}").strip('"')
            if reason == "Revision does not exist":
                raise SchematisationHasNoRevisionsError
        except IndexError:
            raise e

    # sqlite
    sqlite_download = THREEDI_API.schematisations_revisions_sqlite_download(revision.id, schematisation_pk)
    zip_filepath = storage_dir / revision.sqlite.file.filename
    get_download_file(sqlite_download, zip_filepath)

    # rasters
    os.makedirs(storage_dir / "rasters", exist_ok=True)
    rasters_downloads = []
    for raster_file in revision.rasters or []:
        raster_download = download_schematisation_revision_raster(
            raster_pk=raster_file.id, schematisation_pk=schematisation_pk, revision_pk=revision.id
        )
        rasters_downloads.append((raster_file.name, raster_download))
    for raster_filename, raster_download in rasters_downloads:
        raster_filepath = str(storage_dir / "rasters" / raster_filename)
        get_download_file(raster_download, raster_filepath)
