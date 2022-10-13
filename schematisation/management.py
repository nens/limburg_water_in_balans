from threedi_api_client.api import ThreediApi

from constants import THREEDI_API_HOST, ORGANISATION_UUID, ORGANISATION_UUID_NENS
from download_revision import download_latest_revision
from login import get_login_details

CONFIG = {
    "THREEDI_API_HOST": THREEDI_API_HOST,
    "THREEDI_API_USERNAME": get_login_details(option='username'),
    "THREEDI_API_PASSWORD": get_login_details(option='password')
}
THREEDI_API = ThreediApi(config=CONFIG, version='v3-beta')


def list_schematisations(owner_uuid, name_icontains):
    schematisations = THREEDI_API.schematisations_list(
        owner__unique_id=ORGANISATION_UUID_NENS,
        limit=99999,
        name__icontains="v0151"
    )
    for schematisation in schematisations.results:
        print(schematisation.id, schematisation.name, ", ".join(schematisation.tags), schematisation.last_updated, sep="|")


def delete_schematisation(
        schematisation_name,
        schematisation_id,
        owner_uuid,
        backup_path=None
):
    schematisations = THREEDI_API.schematisations_list(
        owner__unique_id=owner_uuid,
        name=schematisation_name
    ).results
    found = False
    for schematisation in schematisations:
        if schematisation.id == schematisation_id:
            found = True
            break
    if not found:
        raise ValueError(f"Schematisation {schematisation_name} does not exist")
    print(f"Deleting schematisation {schematisation.id}: {schematisation.name}")
    revisions = THREEDI_API.schematisations_revisions_list(schematisation_pk=schematisation.id).results
    if backup_path:
        download_revision()
    for revision in revisions:
        threedimodels = THREEDI_API.threedimodels_list(revision__id=revision.id).results
        for threedimodel in threedimodels:
            THREEDI_API.threedimodels_partial_update(id=threedimodel.id, data={"disabled": True})
            THREEDI_API.threedimodels_delete(id=threedimodel.id)
            print(f"deleted threedimodel {threedimodel.name}")
        THREEDI_API.schematisations_revisions_delete(
            id=revision.id,
            schematisation_pk=schematisation.id,
            data={"number": revision.number}
        )
        print(f"deleted revision {revision.id} (nr. {revision.number})")
    THREEDI_API.schematisations_delete(id=schematisation.id)
    print(f"deleted schematisation {schematisation.name}")


if __name__ == "__main__":

    # list_schematisations(owner_uuid=ORGANISATION_UUID_NENS, name_icontains="v0151")
    revision_pk = 19858
    schematisation_pk = 2340
    target_directory = r"C:\Temp"
    download_latest_revision(schematisation_pk=schematisation_pk, target_directory=target_directory)
    # revision = THREEDI_API.schematisations_latest_revision(id=schematisation_pk)
    # print(dir(THREEDI_API))
    # print(revision.number)

    # schematisations_to_delete = [
    # ]
    # delete_schematisation(
    #     schematisation_id=754,
    #     schematisation_name="v0151_banholt - banholt_m_t100_landelijke_neerslag (5)",
    #     owner_uuid=ORGANISATION_UUID_NENS
    # )