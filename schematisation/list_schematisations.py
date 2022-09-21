from threedi_api_client.api import ThreediApi

from constants import THREEDI_API_HOST, ORGANISATION_UUID, ORGANISATION_UUID_NENS
from login import get_login_details

CONFIG = {
    "THREEDI_API_HOST": THREEDI_API_HOST,
    "THREEDI_API_USERNAME": get_login_details(option='username'),
    "THREEDI_API_PASSWORD": get_login_details(option='password')
}
THREEDI_API = ThreediApi(config=CONFIG, version='v3-beta')

# schematisations = THREEDI_API.schematisations_list(owner__unique_id=ORGANISATION_UUID, limit = 99999)
schematisations = THREEDI_API.schematisations_list(
    owner__unique_id=ORGANISATION_UUID_NENS,
    limit=99999,
    name__icontains="v0151"
)
for schematisation in schematisations.results:
    print(schematisation.id, schematisation.name, ", ".join(schematisation.tags), schematisation.last_updated, sep="|")