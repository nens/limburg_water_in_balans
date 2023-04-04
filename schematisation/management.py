from pathlib import Path
from time import sleep
from typing import Union

from threedi_api_client.api import ThreediApi
from threedi_api_client.openapi.exceptions import ApiException

from constants import THREEDI_API_HOST, ORGANISATION_UUID, ORGANISATION_UUID_NENS
from download_revision import download_latest_revision
from exceptions import SchematisationHasNoRevisionsError
from login import get_login_details

CONFIG = {
    "THREEDI_API_HOST": THREEDI_API_HOST,
    "THREEDI_API_USERNAME": get_login_details(option='username'),
    "THREEDI_API_PASSWORD": get_login_details(option='password')
}
THREEDI_API = ThreediApi(config=CONFIG, version='v3-beta')


def list_schematisations(owner_uuid, name_icontains=None, output_file: Union[str, Path] = None, sep: str = ";"):
    if output_file:
        f = open(output_file, "x")
        headers = ["ID", "Schematisation name", "Tags",	"Created by", "Last updated"]
        f.write(sep.join(headers))
        f.write("\n")
    offset = 0
    finished = False
    while not finished:
        schematisations = THREEDI_API.schematisations_list(
            owner__unique_id=owner_uuid,
            limit=99999,
            offset=offset
            # name__icontains=name_icontains
        )
        for schematisation in schematisations.results:
            linelist = [
                schematisation.id,
                schematisation.name,
                ", ".join(schematisation.tags),
                schematisation.created_by_first_name + " " + schematisation.created_by_last_name,
                schematisation.last_updated
            ]
            linelist = [str(i) for i in linelist]
            line = ";".join(linelist)
            if output_file:
                f.write(line)
                f.write("\n")
            else:
                print(line)
        offset += len(schematisations.results)
        finished = schematisations.next is None


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
    if revisions:
        if backup_path:
            try:
                download_latest_revision(schematisation.id, backup_path)
            except SchematisationHasNoRevisionsError:
                print("Schematisation has no committed revisions, not downloading backup data")
        for revision in revisions:
            threedimodels = THREEDI_API.threedimodels_list(revision__id=revision.id).results
            for threedimodel in threedimodels:
                # if not threedimodel.disabled:
                #     # try:
                #     print(f"Disabling threedimodel {threedimodel.id} for revision {revision.id}...")
                #     THREEDI_API.threedimodels_partial_update(id=threedimodel.id, data={"disabled": True})
                #     # except ApiException:
                #     #     pass
                print(f"Deleting threedimodel {threedimodel.id} for revision {revision.id}...")
                THREEDI_API.threedimodels_delete(id=threedimodel.id)
                print(f"deleted threedimodel {threedimodel.name}")
            THREEDI_API.schematisations_revisions_delete(
                id=revision.id,
                schematisation_pk=schematisation.id,
                data={"number": revision.number}
            )
            print(f"deleted revision {revision.id} (nr. {revision.number})")
    else:
        print("Schematisation has no revisions. Proceding with deleting...")
    for i in [1, 5, 30]:
        try:
            THREEDI_API.schematisations_delete(id=schematisation.id)
        except ApiException:
            sleep(i)
    print(f"deleted schematisation {schematisation.name}")


def rename_schematisation(schematisation_id, old_name, new_name):
    schematisation = THREEDI_API.schematisations_read(schematisation_id)
    if schematisation.name == old_name:
        THREEDI_API.schematisations_update(id=schematisation_id, data={"name": new_name})
        print(f"Renamed schematisation {schematisation_id} from '{old_name}' to '{new_name}'")
    else:
        raise ValueError(f"Schematisation {schematisation_id} is not named {old_name}!")


def change_schematisation_owner(schematisation_id, schematisation_name, old_owner_uuid, new_owner_uuid):
    schematisation = THREEDI_API.schematisations_read(schematisation_id)
    if schematisation_name != schematisation.name:
        raise ValueError(f"Schematisation {schematisation_id} is not named {schematisation_name}!")
    if schematisation.owner == old_owner_uuid:
        old_org_list = THREEDI_API.contracts_list(organisation__unique_id=old_owner_uuid).results
        old_org = old_org_list[0].organisation_name if old_org_list else f"UUID {old_owner_uuid}"
        new_org_list = THREEDI_API.contracts_list(organisation__unique_id=new_owner_uuid).results
        new_org = new_org_list[0].organisation_name if new_org_list else f"UUID {new_owner_uuid}"
        THREEDI_API.schematisations_update(
            id=schematisation_id, data={
                "name": schematisation_name,
                "owner": new_owner_uuid
            })
        print(f"Changed ownership of schematisation {schematisation_id} '{schematisation.name}' from '{old_org}' to '{new_org}'")
    else:
        raise ValueError(f"Schematisation {schematisation_id} '{schematisation.name}' is not owned by {old_owner_uuid}!")


if __name__ == "__main__":

    list_schematisations(
        owner_uuid=ORGANISATION_UUID,
        output_file=r"C:\Temp\schematisations_20230105.csv"
    )

    schematisations_to_rename = [
        # (123, "aalbeek-wijnandsrade - Aalbeek-Wijnandsrade_t_compleet (1)", "Aalbeek-Wijnandsrade Gebiedsbreed"),
        # (124, "aalbeek-wijnandsrade - Aalbeek-Wijnandsrade_t_landelijk (2)", "Aalbeek-Wijnandsrade Landelijk"),
        # (125, "aalbeek-wijnandsrade - Aalbeek-Wijnandsrade_t_stedelijk (3)", "Aalbeek-Wijnandsrade Stedelijk"),
        # (5572, "Meerssen Verwacht T100 Gebiedsbreed v2", "Meerssen Verwacht T100 Gebiedsbreed"),
        # (5571, "Meerssen Verwacht T100 Landelijk v2", "Meerssen Verwacht T100 Landelijk"),
        # (5573, "Meerssen Verwacht T100 Stedelijk v2", "Meerssen Verwacht T100 Stedelijk"),
        # (5569, "Meerssen Verwacht T25 Landelijk v2", "Meerssen Verwacht T25 Landelijk"),
        # (5570, "Meerssen Verwacht T25 Stedelijk v2", "Meerssen Verwacht T25 Stedelijk"),
        # (5517, "Noorbeek Huidig", "Noorbeek Huidig T25 Gebiedsbreed"),
        # (5543, "Noorbeek Huidig Landelijk", "Noorbeek Huidig T25 Landelijk"),
        # (5542, "Noorbeek Huidig Stedelijk", "Noorbeek Huidig T25 Stedelijk"),
        # (5595, "Noorbeek Huidig T100", "Noorbeek Huidig T100 Gebiedsbreed"),
        # (145, "w0154_hekerbeekdal - t100_gebiedsbreed (1)", "Hekerbeek T100 Gebiedsbreed"),
        # (146, "w0154_hekerbeekdal - t100_landelijk (2)", "Hekerbeek T100 Landelijk"),
        # (147, "w0154_hekerbeekdal - t100_stedelijk (3)", "Hekerbeek T100 Stedelijk"),
        # (148, "w0154_hekerbeekdal - t25_gebiedsbreed (1)", "Hekerbeek T25 Gebiedsbreed"),
        # (149, "w0154_hekerbeekdal - t25_landelijk (2)", "Hekerbeek T25 Landelijk"),
        # (151, "w0154_hekerbeekdal - t25_maatregel1_gebiedsbreed_inf_1a (1)", "Hekerbeek Maatregel 1A T25 Gebiedsbreed"),
        # (154, "w0154_hekerbeekdal - t25_maatregel1_gebiedsbreed_inf_1b (4)", "Hekerbeek Maatregel 1B T25 Gebiedsbreed"),
        # (152, "w0154_hekerbeekdal - t25_maatregel1_landelijk_inf_1a (2)", "Hekerbeek Maatregel 1A T25 Landelijk"),
        # (155, "w0154_hekerbeekdal - t25_maatregel1_landelijk_inf_1b (5)", "Hekerbeek Maatregel 1B T25 Landelijk"),
        # (153, "w0154_hekerbeekdal - t25_maatregel1_stedelijk__inf_1a (3)", "Hekerbeek Maatregel 1A T25 Stedelijk"),
        # (156, "w0154_hekerbeekdal - t25_maatregel1_stedelijk_inf_1b (6)", "Hekerbeek Maatregel 1B T25 Stedelijk"),
        # (157, "w0154_hekerbeekdal - t25_maatregel2_gebiedsbreed (1)", "Hekerbeek Maatregel 2 T25 Gebiedsbreed"),
        # (158, "w0154_hekerbeekdal - t25_maatregel2_landelijk (2)", "Hekerbeek Maatregel 2 T25 Landelijk"),
        # (159, "w0154_hekerbeekdal - t25_maatregel2_stedelijk (3)", "Hekerbeek Maatregel 2 T25 Stedelijk"),
        # (150, "w0154_hekerbeekdal - t25_stedelijk (3)", "Hekerbeek T25 Stedelijk")
    ]
    for schematisation_id, schematisation_name, new_name in schematisations_to_rename:
        rename_schematisation(
            schematisation_id=schematisation_id,
            old_name=schematisation_name,
            new_name=new_name
        )

    schematisations_to_reown = [
        # (748, "Banholt Mheer T100 Landelijk"),
        # (749, "Banholt Mheer T100 Stedelijk"),
        # (752, "Banholt Mheer T25 Gebiedsbreed"),
        # (750, "Banholt Mheer T25 Landelijk"),
        # (751, "Banholt Mheer T25 Stedelijk"),
        # (801, "Eyserbeek T100 Gebiedsbreed"),
        # (800, "Eyserbeek T100 Landelijk"),
        # (799, "Eyserbeek T100 Stedelijk"),
        # (804, "Eyserbeek T25 Gebiedsbreed"),
        # (803, "Eyserbeek T25 Landelijk"),
        # (802, "Eyserbeek T25 Stedelijk"),
        # (795, "Geleenbeek T100 Gebiedsbreed"),
        # (794, "Geleenbeek T100 Landelijk"),
        # (793, "Geleenbeek T100 Stedelijk"),
        # (798, "Geleenbeek T25 Gebiedsbreed"),
        # (797, "Geleenbeek T25 Landelijk"),
        # (796, "Geleenbeek T25 Stedelijk"),
        # (721, "Geul Midden T100 Gebiedsbreed"),
        # (723, "Geul Midden T100 Landelijk"),
        # (722, "Geul Midden T100 Stedelijk"),
        # (724, "Geul Midden T25 Gebiedsbreed"),
        # (726, "Geul Midden T25 Landelijk"),
        # (725, "Geul Midden T25 Stedelijk"),
        # (729, "Geul Oost T100 Gebiedsbreed"),
        # (733, "Geul Oost T100 Landelijk"),
        # (732, "Geul Oost T100 Stedelijk"),
        # (728, "Geul Oost T25 Gebiedsbreed"),
        # (731, "Geul Oost T25 Landelijk"),
        # (730, "Geul Oost T25 Stedelijk"),
        # (708, "Geul West T100 Gebiedsbreed"),
        # (709, "Geul West T100 Landelijk"),
        # (710, "Geul West T100 Stedelijk"),
        # (711, "Geul West T25 Gebiedsbreed"),
        # (712, "Geul West T25 Landelijk"),
        # (713, "Geul West T25 Stedelijk"),
        # (735, "Grubbe Sibbersloot T100 Gebiedsbreed"),
        # (739, "Grubbe Sibbersloot T100 Landelijk"),
        # (738, "Grubbe Sibbersloot T100 Stedelijk"),
        # (734, "Grubbe Sibbersloot T25 Gebiedsbreed"),
        # (737, "Grubbe Sibbersloot T25 Landelijk"),
        # (736, "Grubbe Sibbersloot T25 Stedelijk"),
        # (671, "Maastricht Oost T100 Gebiedsbreed"),
        # (672, "Maastricht Oost T100 Landelijk"),
        # (673, "Maastricht Oost T100 Stedelijk"),
        # (674, "Maastricht Oost T25 Gebiedsbreed"),
        # (675, "Maastricht Oost T25 Landelijk"),
        # (676, "Maastricht Oost T25 Stedelijk"),
        # (747, "Maastricht West T100 Stedelijk"),
        # (783, "Rode beek T100 Gebiedsbreed"),
        # (782, "Rode beek T100 Landelijk"),
        # (781, "Rode beek T100 Stedelijk"),
        # (786, "Rode beek T25 Gebiedsbreed"),
        # (785, "Rode beek T25 Landelijk"),
        # (784, "Rode beek T25 Stedelijk"),
        # (744, "Termaardergrub-Herkenradergrub T100 Gebiedsbreed"),
        # (742, "Termaardergrub-Herkenradergrub T100 Landelijk"),
        # (743, "Termaardergrub-Herkenradergrub T100 Stedelijk"),
        # (746, "Termaardergrub-Herkenradergrub T25 Gebiedsbreed"),
        # (741, "Termaardergrub-Herkenradergrub T25 Landelijk"),
        # (745, "Termaardergrub-Herkenradergrub T25 Stedelijk"),
        # (773, "Worm T100 Gebiedsbreed"),
        # (777, "Worm T100 Landelijk"),
        # (776, "Worm T100 Stedelijk"),
        # (780, "Worm T25 Gebiedsbreed"),
        # (779, "Worm T25 Landelijk"),
        # (778, "Worm T25 Stedelijk"),
    ]
    for schematisation_id, schematisation_name in schematisations_to_reown:
        change_schematisation_owner(
            schematisation_id=schematisation_id,
            schematisation_name=schematisation_name,
            old_owner_uuid=ORGANISATION_UUID_NENS,
            new_owner_uuid=ORGANISATION_UUID
        )

    schematisations_to_delete = [
        # (5277, "akerloot_hp"),
        # (5271, "Akersloot (Joey)"),
        # (5276, "Akersloot_Edo"),
        # (5272, "Akersloot_joey"),
        # (5275, "Akersloot_joey2"),
        # (491, "eigen_model_joey - selwerd_model_joey (1)"),
        # (5102, "Eygelshoven - Huidig-verbeterd"),
        # (5098, "Eygelshoven - Verwacht"),
        # (5334, "Hekerbeek drempel 10 cm"),
        # (5335, "Hekerbeek drempel 15 cm"),
        # (5336, "Hekerbeek drempel 20 cm"),
        # (5355, "Hekerbeek drempel 30 cm"),
        # (5351, "Hekerbeek drempel 40 cm"),
        # (5305, "Hekerbeek drempel 5 cm"),
        # (5319, "Hekerbeek zonder drempel"),
        # (5309, "Hekerbeekdal drempel 5cm"),
        # (1407, "heugem_limmel_geul_midden - geul_midden_t100 (2)"),
        # (1404, "heugem_limmel_geul_midden - geul_midden_t100_t100 (1)"),
        # (1406, "heugem_limmel_geul_midden - geul_midden_t25 (1)"),
        # (1405, "heugem_limmel_geul_midden - geul_midden_t25_t25 (1)"),
        # (1412, "heugem_limmel_geul_oost - geul_oost_t100 (2)"),
        # (1411, "heugem_limmel_geul_oost - geul_oost_t25 (1)"),
        # (1403, "heugem_limmel_geul_west - geul_west_t100 (2)"),
        # (1398, "heugem_limmel_geul_west - geul_west_t100_t100 (1)"),
        # (1401, "heugem_limmel_geul_west - geul_west_t100_t100 (2)"),
        # (1402, "heugem_limmel_geul_west - geul_west_t25 (1)"),
        # (1400, "heugem_limmel_geul_west - geul_west_t25_t100 (2)"),
        # (1399, "heugem_limmel_geul_west - geul_west_t25_t25 (1)"),
        # (1410, "heugem_limmel_grubbe_sibbersloot - grubbe_sibbersloot_bui9 (3)"),
        # (1409, "heugem_limmel_grubbe_sibbersloot - grubbe_sibbersloot_t100 (2)"),
        # (1408, "heugem_limmel_grubbe_sibbersloot - grubbe_sibbersloot_t25 (1)"),
        # (1397, "heugem_limmel_maastricht_oost - maastricht_oost_t100 (2)"),
        # (1394, "heugem_limmel_maastricht_oost - maastricht_oost_t100_t100 (2)"),
        # (1396, "heugem_limmel_maastricht_oost - maastricht_oost_t25 (1)"),
        # (1395, "heugem_limmel_maastricht_oost - maastricht_oost_t25_t25 (1)"),
        # (1393, "heugem_limmel_termaardergrub_herkenradergrub - termaardergrub_herkenradergrub_t100 (2)"),
        # (1392, "heugem_limmel_termaardergrub_herkenradergrub - termaardergrub_herkenradergrub_t25 (1)"),
        # (1611, "heugem-limmel-integraal-midden - heugem_limmel_integraal_midden_t25 (1)"),
        # (1612, "heugem-limmel-integraal-noord - heugem_limmel_integraal_noord_t25 (1)"),
        # (1609, "heugem-limmel-integraal-zuid - heugem_limmel_integraal_zuid_t100 (1)"),
        # (1610, "heugem-limmel-integraal-zuid - heugem_limmel_integraal_zuid_t100 (2)"),
        # (5544, "Huidig T25  Gebiedsbreed"),
        # (1868, "meerssen - meerssen_bufferpakket_+_landbouw (1)"),
        # (1867, "meerssen - meerssen_bufferpakket_T25-2050 (1)"),
        # (1866, "meerssen - meerssen_huidig (1)"),
        # (1869, "meerssen - meerssen_koker_verruimen (1)"),
        # (1870, "meerssen - meerssen_landbouw_10mmberging (1)"),
        # (1871, "meerssen - meerssen_stedelijk_afkoppelen (1)"),
        # (1872, "meerssen - meerssen_variant1_bufferen_bergen_afkoppelen (1)"),
        # (1873, "meerssen - meerssen_variant2_bufferen_bergen_afkoppelen (1)"),
        # (1874, "meerssen - v2_bergermeer_bres_maalstop (1)"),
        # (5490, "Meerssen Verwacht T100 Gebiedsbreed"),
        # (5492, "Meerssen Verwacht T100 Landelijk"),
        # (5491, "Meerssen Verwacht T100 Stedelijk"),
        # (5489, "Meerssen Verwacht T25 Landelijk"),
        # (5488, "Meerssen Verwacht T25 Stedelijk"),
        # (1622, "meerssen-t25-t100-2050-klimaat - meerssen_t100_validatie (1)"),
        # (1623, "meerssen-t25-t100-2050-klimaat - meerssen_t25_validatie (1)"),
        # (490, "model_joey2 - selwerd_model_joey (1)"),
        # (489, "model_takehome_joey - selwerd_model_joey (1)"),
        # (494, "my_first_model_alo - Selwerd_arnoud (1)"),
        # (160, "w0154_hekerbeekdal - bui8_gebiedsbreed (1)"),
        # (161, "w0154_hekerbeekdal - bui8_landelijk (2)"),
        # (162, "w0154_hekerbeekdal - bui8_stedelijk (3)"),
        # (166, "w0154_hekerbeekdal - geul_oost_t100 (2)"),
        # (165, "w0154_hekerbeekdal - geul_oost_t25 (1)"),
        # (164, "w0154_hekerbeekdal - hekerbeekdal_t100 (2)"),
        # (163, "w0154_hekerbeekdal - hekerbeekdal_t25 (1)"),
        # (142, "w0154_hekerbeekdal - t10_gebiedsbreed (1)"),
        # (143, "w0154_hekerbeekdal - t10_landelijk (2)"),
        # (144, "w0154_hekerbeekdal - t10_stedelijk (3)")
        # (5969, "K:/A_Feenstra/X0143 - Stikstof Limburg/Geul Midden T25/schematisation/Geul Midden T25.sqlite")
    ]
    for schematisation_id, schematisation_name in schematisations_to_delete:
        delete_schematisation(
            schematisation_id=schematisation_id,
            schematisation_name=schematisation_name,
            owner_uuid=ORGANISATION_UUID,
            backup_path=r"C:\Temp"
        )

    for schematisation_id, schematisation_name in [
        # (5969, "K:/A_Feenstra/X0143 - Stikstof Limburg/Geul Midden T25/schematisation/Geul Midden T25.sqlite")
    ]:
        delete_schematisation(
            schematisation_id=schematisation_id,
            schematisation_name=schematisation_name,
            owner_uuid=ORGANISATION_UUID
        )



