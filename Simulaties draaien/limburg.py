# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 09:27:01 2022

@author: Kizje.marif

This script contains the required functions to start a simulations and download the results via the 
api of 3Di. 

"""

from datetime import datetime
from time import sleep
import pandas as pd

import pytz
from threedi_api_client.openapi import ApiException
from threedi_api_client.api import ThreediApi

from threedi_scenario_downloader import downloader as dl
import os

from constants import *

from login import get_login_details

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

starttime_dt = datetime(2021, 1, 1, 0, 0, 0, 0) #zet op 1 januari zodat alle simaties dezelfde start en eindtijd hebben. 
starttime = pd.Series(starttime_dt).dt.round("30T")[0]


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
        duration=3.5 * 60 * 60
):
    print(bui)
    model, simulation_name = get_model_and_simulation_name(schematisation_name=schematisation_name, bui=bui)

    # find simulation template
    simulation_template = THREEDI_API.simulation_templates_list(simulation__threedimodel__id=model.id).results[0]
    simulation = THREEDI_API.simulations_from_template(
        data={
            "template": simulation_template.id,
            "name": simulation_name,
            "tags": ["W0154"],
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
        raise ValueError("Kies 'T100' of 'Radar' als bui")

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
    api_client = ThreediApiClient(config=CONFIG)
    simulation_api = SimulationsApi(api_client)
    simulation_api.simulations_actions_create(sim_id, data={"name": "shutdown"})
    return


paths = r"G:\Projecten W (2021)\W0154 - Hekerbeekdal actualisatie en maatregelverkenning, Waterschap Limburg\Gegevens\Bewerking\Rekenresultaten"

#%%

def download_results(schematisation_name: str,bui: str = 'T25'):
    dl.set_api_key("x3sGSny8.jaVsJj2gA2P7PnAdut3usTZEk7qW2Tmp")
    scenario_name = get_model_and_simulation_name(schematisation_name=schematisation_name, bui=bui)[1]
    create_folder = os.makedirs(paths+str(scenario_name), exist_ok=True)
    results_folder = str(paths)+str(scenario_name)
    scenarios = dl.find_scenarios_by_name(scenario_name,limit=100)
    scenario_uuid = scenarios[0]['uuid']
    print ('start download of' + scenario_name)
    dl.download_raw_results(scenario_uuid,pathname=os.path.join(results_folder,"results_3di.nc"))
    dl.download_grid_administration(scenario_uuid,pathname=os.path.join(results_folder,"gridadmin.h5"))
    dl.download_maximum_waterdepth_raster(scenario_uuid,"EPSG:28992",0.5,pathname=os.path.join(results_folder,scenario_name+"_max_depth.tif"))
    dl.download_raster(scenario_uuid,"ucr-max-quad","EPSG:28992",10,pathname=os.path.join(results_folder,scenario_name+"_max_velocity.tif"))
    log_url = dl.get_logging_link((scenarios[0]['uuid']))
    dl.download_file(log_url, path=os.path.join(results_folder, 'log.zip'))         
    agg_url = dl.get_aggregation_netcdf_link((scenarios[0]['uuid']))
    dl.download_file(agg_url, path=os.path.join(results_folder, 'aggregate_results_3di.nc'))
    return

if __name__ == "__main__":
    for bui in ["T25"]:
        for schem in SCHEMATISATIONS:
            start_simulatie(schematisation_name=schem, bui=bui)
          #  download_results(schematisation_name=schem, bui=bui)
















