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
        owner__unique_id=owner_uuid,
        limit=99999,
        name__icontains=name_icontains
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
    if revisions:
        if backup_path:
            download_latest_revision(schematisation.id, backup_path)
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
    else:
        print("Schematisation has no revisions. Proceding with deleting...")
    THREEDI_API.schematisations_delete(id=schematisation.id)
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

    # list_schematisations(owner_uuid=ORGANISATION_UUID_NENS, name_icontains="v0151")
    revision_pk = 19858
    schematisation_pk = 2340

    schematisations_to_rename = [
        (748, "v0151_banholt - banholt_m_t100_landelijke_neerslag (1)", "Banholt Mheer T100 Landelijk"),
        (749, "v0151_banholt - banholt_m_t100_stedelijke_neerslag (2)", "Banholt Mheer T100 Stedelijk"),
        (752, "v0151_banholt - banholt_m_t25_gebiedbrede_neerslag (6)", "Banholt Mheer T25 Gebiedsbreed"),
        (750, "v0151_banholt - banholt_m_t25_landelijke_neerslag (3)", "Banholt Mheer T25 Landelijk"),
        (751, "v0151_banholt - banholt_m_t25_stedelijke_neerslag (4)", "Banholt Mheer T25 Stedelijk"),
        (801, "v0151_eyserbeek - eyserbeek_m_t100_gebiedsbrede_neerslag (3)", "Eyserbeek T100 Gebiedsbreed"),
        (800, "v0151_eyserbeek - eyserbeek_m_t100_landelijke_neerslag (2)", "Eyserbeek T100 Landelijk"),
        (799, "v0151_eyserbeek - eyserbeek_m_t100_stedelijke_neerslag (1)", "Eyserbeek T100 Stedelijk"),
        (804, "v0151_eyserbeek - eyserbeek_m_t25_gebiedsbrede_neerslag (6)", "Eyserbeek T25 Gebiedsbreed"),
        (803, "v0151_eyserbeek - eyserbeek_m_t25_landelijke_neerslag (5)", "Eyserbeek T25 Landelijk"),
        (802, "v0151_eyserbeek - eyserbeek_m_t25_stedelijke_neerslag (4)", "Eyserbeek T25 Stedelijk"),
        (795, "v0151_geleenbeek - geleenbeek_m_t100_gebiedsbrede_neerslag (3)", "Geleenbeek T100 Gebiedsbreed"),
        (794, "v0151_geleenbeek - geleenbeek_m_t100_landelijke_neerslag (2)", "Geleenbeek T100 Landelijk"),
        (793, "v0151_geleenbeek - geleenbeek_m_t100_stedelijke_neerslag (1)", "Geleenbeek T100 Stedelijk"),
        (798, "v0151_geleenbeek - geleenbeek_m_t25_gebiedsbrede_neerslag (6)", "Geleenbeek T25 Gebiedsbreed"),
        (797, "v0151_geleenbeek - geleenbeek_m_t25_landelijke_neerslag (5)", "Geleenbeek T25 Landelijk"),
        (796, "v0151_geleenbeek - geleenbeek_m_t25_stedelijke_neerslag (4)", "Geleenbeek T25 Stedelijk"),
        (721, "v0151_geul_midden_t100 - geul_midden_t100_t100 (1)", "Geul Midden T100 Gebiedsbreed"),
        (723, "v0151_geul_midden_t100 - geul_midden_t100_t100_landelijk (3)", "Geul Midden T100 Landelijk"),
        (722, "v0151_geul_midden_t100 - geul_midden_t100_t100_stedelijk (2)", "Geul Midden T100 Stedelijk"),
        (724, "v0151_geul_midden_t25 - geul_midden_t25_t25 (1)", "Geul Midden T25 Gebiedsbreed"),
        (726, "v0151_geul_midden_t25 - geul_midden_t25_t25_landelijk (3)", "Geul Midden T25 Landelijk"),
        (725, "v0151_geul_midden_t25 - geul_midden_t25_t25_stedelijk (2)", "Geul Midden T25 Stedelijk"),
        (729, "v0151_geul_oost - geul_oost_t100 (2)", "Geul Oost T100 Gebiedsbreed"),
        (733, "v0151_geul_oost - geul_oost_t100_landelijk (6)", "Geul Oost T100 Landelijk"),
        (732, "v0151_geul_oost - geul_oost_t100_stedelijk (5)", "Geul Oost T100 Stedelijk"),
        (728, "v0151_geul_oost - geul_oost_t25 (1)", "Geul Oost T25 Gebiedsbreed"),
        (731, "v0151_geul_oost - geul_oost_t25_landelijk (4)", "Geul Oost T25 Landelijk"),
        (730, "v0151_geul_oost - geul_oost_t25_stedelijk (3)", "Geul Oost T25 Stedelijk"),
        (708, "v0151_geul_west_t100 - geul_west_t100_t100 (1)", "Geul West T100 Gebiedsbreed"),
        (709, "v0151_geul_west_t100 - geul_west_t100_t100_landelijk (2)", "Geul West T100 Landelijk"),
        (710, "v0151_geul_west_t100 - geul_west_t100_t100_stedelijk (3)", "Geul West T100 Stedelijk"),
        (711, "v0151_geul_west_t25 - geul_west_t25_t25 (1)", "Geul West T25 Gebiedsbreed"),
        (712, "v0151_geul_west_t25 - geul_west_t25_t25_landelijke_neerslag (2)", "Geul West T25 Landelijk"),
        (713, "v0151_geul_west_t25 - geul_west_t25_t25_stedelijke_neerslag (3)", "Geul West T25 Stedelijk"),
        (735, "v0151_grubbe_sibbersloot - grubbe_sibbersloot_t100 (2)", "Grubbe Sibbersloot T100 Gebiedsbreed"),
        (739, "v0151_grubbe_sibbersloot - grubbe_sibbersloot_t100_landelijk (6)", "Grubbe Sibbersloot T100 Landelijk"),
        (738, "v0151_grubbe_sibbersloot - grubbe_sibbersloot_t100_stedelijk (5)", "Grubbe Sibbersloot T100 Stedelijk"),
        (734, "v0151_grubbe_sibbersloot - grubbe_sibbersloot_t25 (1)", "Grubbe Sibbersloot T25 Gebiedsbreed"),
        (737, "v0151_grubbe_sibbersloot - grubbe_sibbersloot_t25_landelijk (4)", "Grubbe Sibbersloot T25 Landelijk"),
        (736, "v0151_grubbe_sibbersloot - grubbe_sibbersloot_t25_stedelijk (3)", "Grubbe Sibbersloot T25 Stedelijk"),
        (671, "v0151_maastricht_oost_t100 - maastricht_oost_t100_t100_gebiedsbreed (2)",
         "Maastricht Oost T100 Gebiedsbreed"),
        (672, "v0151_maastricht_oost_t100 - maastricht_oost_t100_t100_landelijk (3)", "Maastricht Oost T100 Landelijk"),
        (673, "v0151_maastricht_oost_t100 - maastricht_oost_t100_t100_stedelijk (4)", "Maastricht Oost T100 Stedelijk"),
        (674, "v0151_maastricht_oost_t25 - maastricht_oost_t25_t25_gebiedsbreed (1)",
         "Maastricht Oost T25 Gebiedsbreed"),
        (675, "v0151_maastricht_oost_t25 - maastricht_oost_t25_t25_landelijk (2)", "Maastricht Oost T25 Landelijk"),
        (676, "v0151_maastricht_oost_t25 - maastricht_oost_t25_t25_stedelijk (3)", "Maastricht Oost T25 Stedelijk"),
        (747, "v0151_maastricht_west - maastricht_west_m_t100_stedelijke_neerslag (19)",
         "Maastricht West T100 Stedelijk"),
        (783, "v0151_rodebeek - rodebeek_t100_gebiedsbrede_neerslag (3)", "Rode beek T100 Gebiedsbreed"),
        (782, "v0151_rodebeek - rodebeek_t100_landelijke_neerslag (2)", "Rode beek T100 Landelijk"),
        (781, "v0151_rodebeek - rodebeek_t100_stedelijke_neerslag (1)", "Rode beek T100 Stedelijk"),
        (786, "v0151_rodebeek - rodebeek_t25_gebiedsbrede_neerslag (6)", "Rode beek T25 Gebiedsbreed"),
        (785, "v0151_rodebeek - rodebeek_t25_landelijke_neerslag (5)", "Rode beek T25 Landelijk"),
        (784, "v0151_rodebeek - rodebeek_t25_stedelijke_neerslag (4)", "Rode beek T25 Stedelijk"),
        (744, "v0151_termaardergrub_herkenradergrub - termaardergrub_herkenradergrub_t100_gebiedbrede_neerslag (4)",
         "Termaardergrub-Herkenradergrub T100 Gebiedsbreed"),
        (742, "v0151_termaardergrub_herkenradergrub - termaardergrub_herkenradergrub_t100_landelijke_neerslag (2)",
         "Termaardergrub-Herkenradergrub T100 Landelijk"),
        (743, "v0151_termaardergrub_herkenradergrub - termaardergrub_herkenradergrub_t100_stedelijke_neerslag (3)",
         "Termaardergrub-Herkenradergrub T100 Stedelijk"),
        (746, "v0151_termaardergrub_herkenradergrub - termaardergrub_herkenradergrub_t25_gebiedbrede_neerslag (6)",
         "Termaardergrub-Herkenradergrub T25 Gebiedsbreed"),
        (741, "v0151_termaardergrub_herkenradergrub - termaardergrub_herkenradergrub_t25_landelijke_neerslag (1)",
         "Termaardergrub-Herkenradergrub T25 Landelijk"),
        (745, "v0151_termaardergrub_herkenradergrub - termaardergrub_herkenradergrub_t25_stedelijke_neerslag (5)",
         "Termaardergrub-Herkenradergrub T25 Stedelijk"),
        (773, "v0151_worm - worm_t100_gebiedsbrede_neerslag (3)", "Worm T100 Gebiedsbreed"),
        (777, "v0151_worm - worm_t100_landelijke_neerslag (2)", "Worm T100 Landelijk"),
        (776, "v0151_worm - worm_t100_stedelijke_neerslag (1)", "Worm T100 Stedelijk"),
        (780, "v0151_worm - worm_t25_gebiedsbrede_neerslag (6)", "Worm T25 Gebiedsbreed"),
        (779, "v0151_worm - worm_t25_landelijke_neerslag (5)", "Worm T25 Landelijk"),
        (778, "v0151_worm - worm_t25_stedelijke_neerslag (4)", "Worm T25 Stedelijk"),
    ]
    for schematisation_id, schematisation_name, new_name in schematisations_to_rename:
        rename_schematisation(
            schematisation_id=schematisation_id,
            old_name=schematisation_name,
            new_name=new_name
        )

    schematisations_to_reown = [
        (748, "Banholt Mheer T100 Landelijk"),
        (749, "Banholt Mheer T100 Stedelijk"),
        (752, "Banholt Mheer T25 Gebiedsbreed"),
        (750, "Banholt Mheer T25 Landelijk"),
        (751, "Banholt Mheer T25 Stedelijk"),
        (801, "Eyserbeek T100 Gebiedsbreed"),
        (800, "Eyserbeek T100 Landelijk"),
        (799, "Eyserbeek T100 Stedelijk"),
        (804, "Eyserbeek T25 Gebiedsbreed"),
        (803, "Eyserbeek T25 Landelijk"),
        (802, "Eyserbeek T25 Stedelijk"),
        (795, "Geleenbeek T100 Gebiedsbreed"),
        (794, "Geleenbeek T100 Landelijk"),
        (793, "Geleenbeek T100 Stedelijk"),
        (798, "Geleenbeek T25 Gebiedsbreed"),
        (797, "Geleenbeek T25 Landelijk"),
        (796, "Geleenbeek T25 Stedelijk"),
        (721, "Geul Midden T100 Gebiedsbreed"),
        (723, "Geul Midden T100 Landelijk"),
        (722, "Geul Midden T100 Stedelijk"),
        (724, "Geul Midden T25 Gebiedsbreed"),
        (726, "Geul Midden T25 Landelijk"),
        (725, "Geul Midden T25 Stedelijk"),
        (729, "Geul Oost T100 Gebiedsbreed"),
        (733, "Geul Oost T100 Landelijk"),
        (732, "Geul Oost T100 Stedelijk"),
        (728, "Geul Oost T25 Gebiedsbreed"),
        (731, "Geul Oost T25 Landelijk"),
        (730, "Geul Oost T25 Stedelijk"),
        (708, "Geul West T100 Gebiedsbreed"),
        (709, "Geul West T100 Landelijk"),
        (710, "Geul West T100 Stedelijk"),
        (711, "Geul West T25 Gebiedsbreed"),
        (712, "Geul West T25 Landelijk"),
        (713, "Geul West T25 Stedelijk"),
        (735, "Grubbe Sibbersloot T100 Gebiedsbreed"),
        (739, "Grubbe Sibbersloot T100 Landelijk"),
        (738, "Grubbe Sibbersloot T100 Stedelijk"),
        (734, "Grubbe Sibbersloot T25 Gebiedsbreed"),
        (737, "Grubbe Sibbersloot T25 Landelijk"),
        (736, "Grubbe Sibbersloot T25 Stedelijk"),
        (671, "Maastricht Oost T100 Gebiedsbreed"),
        (672, "Maastricht Oost T100 Landelijk"),
        (673, "Maastricht Oost T100 Stedelijk"),
        (674, "Maastricht Oost T25 Gebiedsbreed"),
        (675, "Maastricht Oost T25 Landelijk"),
        (676, "Maastricht Oost T25 Stedelijk"),
        (747, "Maastricht West T100 Stedelijk"),
        (783, "Rode beek T100 Gebiedsbreed"),
        (782, "Rode beek T100 Landelijk"),
        (781, "Rode beek T100 Stedelijk"),
        (786, "Rode beek T25 Gebiedsbreed"),
        (785, "Rode beek T25 Landelijk"),
        (784, "Rode beek T25 Stedelijk"),
        (744, "Termaardergrub-Herkenradergrub T100 Gebiedsbreed"),
        (742, "Termaardergrub-Herkenradergrub T100 Landelijk"),
        (743, "Termaardergrub-Herkenradergrub T100 Stedelijk"),
        (746, "Termaardergrub-Herkenradergrub T25 Gebiedsbreed"),
        (741, "Termaardergrub-Herkenradergrub T25 Landelijk"),
        (745, "Termaardergrub-Herkenradergrub T25 Stedelijk"),
        (773, "Worm T100 Gebiedsbreed"),
        (777, "Worm T100 Landelijk"),
        (776, "Worm T100 Stedelijk"),
        (780, "Worm T25 Gebiedsbreed"),
        (779, "Worm T25 Landelijk"),
        (778, "Worm T25 Stedelijk"),
    ]
    for schematisation_id, schematisation_name in schematisations_to_reown:
        change_schematisation_owner(
            schematisation_id=schematisation_id,
            schematisation_name=schematisation_name,
            old_owner_uuid=ORGANISATION_UUID_NENS,
            new_owner_uuid=ORGANISATION_UUID
        )

    schematisations_to_delete = [
        (754, "v0151_banholt - banholt_m_t100_landelijke_neerslag (5)"),
        (789, "v0151_geul - geul_m_t100_gebiedsbrede_neerslag (3)"),
        (788, "v0151_geul - geul_m_t100_landelijke_neerslag (2)"),
        (787, "v0151_geul - geul_m_t100_stedelijke_neerslag (1)"),
        (792, "v0151_geul - geul_m_t25_gebiedsbrede_neerslag (6)"),
        (791, "v0151_geul - geul_m_t25_landelijke_neerslag (5)"),
        (790, "v0151_geul - geul_m_t25_stedelijke_neerslag (4)"),
        (716, "v0151_maastricht_oost - maastricht_oost_t100 (2)"),
        (720, "v0151_maastricht_oost - maastricht_oost_t100_landelijk (6)"),
        (719, "v0151_maastricht_oost - maastricht_oost_t100_stedelijk (5)"),
        (715, "v0151_maastricht_oost - maastricht_oost_t25 (1)"),
        (718, "v0151_maastricht_oost - maastricht_oost_t25_landelijk (4)"),
        (717, "v0151_maastricht_oost - maastricht_oost_t25_stedelijk (3)"),
        (774, "v0151_worm - worm_10x4_t100_gebiedsbrede_neerslag (3)"),
        (775, "v0151_worm - worm_5x4_t100_gebiedsbrede_neerslag (3)"),
    ]
    for schematisation_id, schematisation_name in schematisations_to_delete:
        delete_schematisation(
            schematisation_id=schematisation_id,
            schematisation_name=schematisation_name,
            owner_uuid=ORGANISATION_UUID_NENS,
            backup_path=r"C:\Temp"
        )

