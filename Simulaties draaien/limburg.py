# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 09:27:01 2022

@author: Kizje.marif

This script contains the required functions to start a simulations and download the results via the 
api of 3Di. 

"""

from datetime import datetime
from time import sleep
from typing import Union, List
from pathlib import Path

import pytz
from threedi_api_client.openapi import ApiException
from threedi_api_client.api import ThreediApi

from threedi_scenario_downloader import downloader as dl
import os

from constants import *
from constants import ORGANISATION_UUID_NENS

from login import get_login_details

CONFIG = {
    "THREEDI_API_HOST": THREEDI_API_HOST_STAGING,
    "THREEDI_API_PERSONAL_API_TOKEN": get_login_details(option='api_key')
}
THREEDI_API = ThreediApi(config=CONFIG, version='v3-beta')

# Define timezones
AMSTERDAM = pytz.timezone('Europe/Amsterdam')
UTC = pytz.utc

# Define start/end date
SIMULATION_START = datetime(2021, 1, 1, 1, 0).astimezone(AMSTERDAM)

starttime_dt = datetime(2021, 1, 1, 0, 0, 0, 0)  # 1 januari zodat alle simaties dezelfde start en eindtijd hebben.


def get_model_and_simulation_name(schematisation_name: str, revision=None, bui: str = 'T25'):
    # find model

    model = THREEDI_API.threedimodels_list(
        limit=1,
        revision__schematisation__name=schematisation_name,
        revision__number=revision
    ).results[0]  # index 0 is always latest revision

    # construct simulation name
    return model, f"{schematisation_name} rev {model.revision_number} {bui}"


def start_simulatie(
        schematisation_name: str,
        revision: int = None,
        bui: str = None,
        initial_waterlevel: int = None,
        duration=3.5 * 60 * 60,
        time_step=None,
        output_time_step=None,
        template_name: str = None,
        post_processing: bool = True,
        tags: List = None,
        billing_goes_to: str = None
):
    print(bui)
    model, simulation_name = get_model_and_simulation_name(
        schematisation_name=schematisation_name,
        revision=revision,
        bui=bui or "droog"
    )

    # find simulation template
    if template_name:
        simulation_template = THREEDI_API.simulation_templates_list(
            simulation__threedimodel__id=model.id,
            name=template_name
        ).results[0]
    else:
        simulation_template = THREEDI_API.simulation_templates_list(simulation__threedimodel__id=model.id).results[0]
    simulation = THREEDI_API.simulations_from_template(
        data={
            "template": simulation_template.id,
            "name": simulation_name,
            "tags": tags or [],
            "organisation": billing_goes_to or ORGANISATION_UUID,
            "start_datetime": SIMULATION_START.astimezone(pytz.utc),
            "duration": duration
        }
    )
    settings = THREEDI_API.simulations_settings_overview(simulation_pk=simulation.id)
    timestep_settings = settings.time_step_settings
    if time_step:
        timestep_settings.time_step = time_step
    if output_time_step:
        timestep_settings.output_time_step = output_time_step

    THREEDI_API.simulations_settings_time_step_partial_update(
        simulation.id,
        timestep_settings
    )

    # add rain
    
    if bui == "T10":
        THREEDI_API.simulations_events_rain_timeseries_create(
                simulation_pk=simulation.id,
                data={
                    "offset": 0,
                    "interpolate": False,
                    "values": BUIEN[bui],
                    "units": "m/s",
                },
            )
    
    elif bui == "T25":
        THREEDI_API.simulations_events_rain_timeseries_create(
                simulation_pk=simulation.id,
                data={
                    "offset": 0,
                    "interpolate": False,
                    "values": BUIEN[bui],
                    "units": "m/s",
                },
            )

    elif bui == "T100":
        THREEDI_API.simulations_events_rain_timeseries_create(
                simulation_pk=simulation.id,
                data={
                    "offset": 0,
                    "interpolate": False,
                    "values": BUIEN[bui],
                    "units": "m/s",
                },
            )

    elif (bui or "").upper() == "RADAR":
        THREEDI_API.simulations_events_rain_rasters_lizard_create(
            simulation.id,
            data=
            {
                "offset": 0,
                "duration": duration,
                "reference_uuid": RADAR_ID,
                "start_datetime": SIMULATION_START.astimezone(pytz.utc),
                "units": "m/s",
                "multiplier": 1
             }
        )
    else:
        print("WARNING: Er wordt geen bui gebruikt")
        # raise ValueError("Kies 'T100' of 'Radar' als bui")

    if initial_waterlevel:
        # read json file
        # initial_water_level_file = Path(initial_water_level_file)
        # with open(initial_water_level_file, 'r') as f:
        #     data = json.load(f)
        # upload_response = THREEDI_API.threedimodels_initial_waterlevels_create(
        #     simulation.id, data={
        #         "filename": initial_water_level_file.name
        #     }
        # )
        # requests.put(upload_response.put_url, data=json.dumps(data))

        THREEDI_API.simulations_initial_1d_water_level_file_create(
            simulation.id, data={"initial_waterlevel": initial_waterlevel}
        )

    # add lizard postprocessing
    if post_processing:
        THREEDI_API.simulations_results_post_processing_lizard_basic_create(
            simulation_pk=simulation.id,
            data={
                "scenario_name": simulation_name,
                "process_basic_results": True,
            }
        )

    # start simulatie
    started = False
    while not started:
        try:
            THREEDI_API.simulations_actions_create(simulation.id, data={"name": "start", "max_rate": 999999})
            print(f"Started simulation {simulation_name} (id {simulation.id}) with model {model.name}")
            started = True
        except ApiException:
            sleep(60)


def end_simulation(sim_id):
    THREEDI_API.simulations_actions_create(sim_id, data={"name": "shutdown"})
    return


def download_results(
        directory: Union[str, Path],
        schematisation_name: str,
        bui: str,
        pixel_size: float,
        raw_results: bool = True,
        max_depth: bool = True,
        max_velocity: bool = True,

):
    directory = Path(directory)
    api_key = get_login_details(section="lizard", option='api_key')
    dl.set_api_key(api_key=api_key)
    scenario_name = get_model_and_simulation_name(schematisation_name=schematisation_name, bui=bui)[1]
    os.makedirs(directory / scenario_name, exist_ok=True)
    results_folder = directory / scenario_name
    scenarios = dl.find_scenarios_by_name(scenario_name, limit=100)
    scenario_uuid = scenarios[0]['uuid']
    print('start download of ' + scenario_name)
    if raw_results:
        dl.download_raw_results(scenario_uuid, pathname=str(results_folder / "results_3di.nc"))
        dl.download_grid_administration(scenario_uuid, pathname=str(results_folder / "gridadmin.h5"))
        log_url = dl.get_logging_link((scenarios[0]['uuid']))
        dl.download_file(log_url, path=str(results_folder / 'log.zip'))
        agg_url = dl.get_aggregation_netcdf_link((scenarios[0]['uuid']))
        dl.download_file(agg_url, path=str(results_folder / 'aggregate_results_3di.nc'))

    if max_depth:
        dl.download_maximum_waterdepth_raster(
            scenario_uuid,
            "EPSG:28992",
            0.5,
            pathname=str(results_folder / str(scenario_name + "_max_depth.tif"))
        )

    if max_velocity:
        dl.download_raster(
            scenario_uuid,
            "ucr-max-quad",
            "EPSG:28992",
            10,
            pathname=str(results_folder / str(scenario_name + "_max_velocity.tif"))
        )
    return


if __name__ == "__main__":
    # directory=r"G:\Projecten W (2021)\W0154 - Hekerbeekdal actualisatie en maatregelverkenning, Waterschap Limburg\Gegevens\Resultaat\Onderdeel C\Dammen Nicolaes\v2"
    # directory = r"C:\Users\leendert.vanwolfswin\Downloads\nicolaes"
    # end_simulation(106242)
    end_simulation(27112)
    start_simulatie(
        schematisation_name="Calamiteitenmodel Delfland (staging)",
        duration=3 * 24 * 60 * 60,
        initial_waterlevel=1430,
        billing_goes_to=ORGANISATION_UUID_NENS
    )
    # for bui in ["T25"]:
    #     for schem in [
    #         "Noorbeek Huidig T25 Gebiedsbreed",
    #         # "Hekerbeek na maatregelen Stedelijk T25",
    #         # "Hekerbeek na maatregelen Landelijk T25"
    #     ]:
    #         start_simulatie(
    #             schematisation_name=schem,
    #             bui=bui,
    #             duration=5*60*60
    #         )
    # for bui in ["T100"]:
    #     for schem in [
    #         "Noorbeek Huidig T100 Gebiedsbreed",
    #         # "Hekerbeek na maatregelen Stedelijk T25",
    #         # "Hekerbeek na maatregelen Landelijk T25"
    #     ]:
    #         start_simulatie(
    #             schematisation_name=schem,
    #             bui=bui,
    #             duration=5 * 60 * 60
    #         )
            # start_simulatie(
            #     schematisation_name=schem,
            #     bui=bui,
            #     duration=5*60*60,
            #     output_time_step=300,
            #     revision=13
            # )
            # download_results(
            #     directory=directory,
            #     schematisation_name=schem,
            #     bui=bui,
            #     pixel_size=0.5
            # )
