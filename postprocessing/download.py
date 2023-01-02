# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 09:27:01 2022

@author: Kizje.marif

This script contains the required functions to start a simulations and download the results via the 
api of 3Di. 

"""

from datetime import datetime
from time import sleep

import pytz
from threedi_api_client.openapi import ApiException
from threedi_api_client.api import ThreediApi

from threedi_scenario_downloader import downloader as dl
import os

from constants import *

from login import get_login_details

api_key = get_login_details(section='lizard', option='api_key')
api_key = ' '
dl.set_api_key(api_key)
CONFIG = {
    "THREEDI_API_HOST": THREEDI_API_HOST,
    "THREEDI_API_USERNAME": get_login_details(option='username'),
    "THREEDI_API_PASSWORD": get_login_details(option='password')
}  #
THREEDI_API = ThreediApi(config=CONFIG, version='v3-beta')

# Define timezones
AMSTERDAM = pytz.timezone('Europe/Amsterdam')
UTC = pytz.utc

# Define start/end date
SIMULATION_START = datetime(2021, 1, 1, 1, 0).astimezone(AMSTERDAM)
PATHS = "/mnt/results/Projecten_X_2022/x0143_stikstof"
grid_space = 1

def get_model_and_simulation_name(schematisation_name: str, bui: str = 'T25'):
    # find model
    model = THREEDI_API.threedimodels_list(
        limit=1,
        revision__schematisation__name=schematisation_name
    ).results[0]  # index 0 is always latest revision
    
    # construct simulation name
    return model, f"{schematisation_name} rev {model.revision_number} {bui}"


def start_simulatie(
        schematisation_name: str,
        bui: str = 'T25',
        duration=6 * 60 * 60
):
    print(bui)
    model, simulation_name = get_model_and_simulation_name(schematisation_name=schematisation_name, bui=bui)

    # find simulation template
    simulation_template = THREEDI_API.simulation_templates_list(simulation__threedimodel__id=model.id).results[0]
    simulation = THREEDI_API.simulations_from_template(
        data={
            "template": simulation_template.id,
            "name": simulation_name,
            "tags": ["X0047"],
            "organisation": ORGANISATION_UUID,
            "start_datetime": SIMULATION_START.astimezone(pytz.utc),
            "duration": duration
        }
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

    elif bui.upper() == "RADAR":
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
        raise ValueError("Kies 'T25' of 'Radar' als bui")

    # add lizard postprocessing
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
            THREEDI_API.simulations_actions_create(simulation.id, data={"name": "queue"})
            print(f"Started simulation {simulation_name} with model {model.name}")
            started = True
        except ApiException:
            sleep(60)


def end_simulation(sim_id):
    THREEDI_API.simulations_actions_create(sim_id, data={"name": "shutdown"})
    return


def download_results(schematisation_name: str,bui: str = 'T25'):
    scenario_name = get_model_and_simulation_name(schematisation_name=schematisation_name, bui=bui)[1]
    out_path = os.path.join(PATHS, schem, bui, scen, 'Results')
    print (out_path)
    results_folder = out_path
    os.makedirs(results_folder, exist_ok=True)
    scenarios = dl.find_scenarios_by_name(scenario_name,limit=100)
    scenario_uuid = scenarios[0]['uuid']
    print ('start download of ' + scenario_name)
    dl.download_raw_results(scenario_uuid,pathname=os.path.join(results_folder,"results_3di.nc"))
    print ('Finished downloading raw results')
    dl.download_grid_administration(scenario_uuid, pathname=os.path.join(results_folder,"gridadmin.h5"))
    print ('Finished downloading grid admin')
    dl.download_maximum_waterdepth_raster(
        scenario_uuid,
        "EPSG:28992",
        grid_space,
        pathname=os.path.join(results_folder,scenario_name+"_max_depth.tif")
    )
    print ('Finished downloading max water depth raster')
    # dl.download_raster(
    #     scenario_uuid,
    #     "ucr-max-quad",
    #     "EPSG:28992",
    #     10,
    #     pathname=os.path.join(results_folder,scenario_name+"_max_velocity.tif")
    # )
    log_url = dl.get_logging_link((scenarios[0]['uuid']))
    dl.download_file(log_url, path=os.path.join(results_folder, 'log.zip'))
    print ('Finished downloading log file')         
    agg_url = dl.get_aggregation_netcdf_link((scenarios[0]['uuid']))
    dl.download_file(agg_url, path=os.path.join(results_folder, 'aggregate_results_3di.nc'))
    print ('Finished downloading aggregate results')
    print ('Finished downloading necessary files for' + scenario_name)
    return

if __name__ == "__main__":
    for bui in ["T25"]:
        for schem in [
        "Geul_Midden"
        ]:
            for scen in ["25p","50p","75p","100p"]:
                schem_name = schem+' '+bui+' '+scen
                get_model_and_simulation_name(schematisation_name=schem_name, bui= 'T25')
                download_results(schematisation_name=schem_name, bui=bui)
            

