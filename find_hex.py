import requests
import os
import json
import datetime

#-----------------------------
# The main file of the tool
#-----------------------------
# This file will be the place for looking up
# MODE S code of an aircraft
# from a certain aircraft registration

#-----------------------------
# Notes
#-----------------------------
#  https://registry.faa.gov/AircraftInquiry/Search/NNumberResult
#  https://forum.flightradar24.com/forum/radar-forums/flightradar24-aircraft-database/10540-aircraft-register-lookup-pages

#-----------------------------
# Flags
#-----------------------------
DEBUG = False
SAVE_RESPONSE = True

#-----------------------------
# directories
#-----------------------------


if __name__ == '__main__':

    print('Not Implemented')
    exit()

    #-----------------------------
    # Constants
    #-----------------------------
    REG_ID = 'N877BR'
    FLIGHT_ID = '2cba8d3f'

    #-----------------------------
    # target url
    #-----------------------------
    HEX_URL_TEMPLATE = 'https://globe.adsbexchange.com/?icao=[HEX]'
    FLIGHT_URL_TEMPLATE = 'https://globe.adsbexchange.com/globe_history/[Y]/[M]/[D]/traces/[HEX-2]/trace_full_[HEX].json'

    #-----------------------------
    # directories
    #-----------------------------
    WORKING_DIR = os.path.dirname(os.path.realpath(__file__))

    os.makedirs(os.path.join(WORKING_DIR, 'Responses'), exist_ok=True)
    os.makedirs(os.path.join(WORKING_DIR, 'GPXs'), exist_ok=True)
    os.makedirs(os.path.join(WORKING_DIR, 'KMLs'), exist_ok=True)

    RESPONSE1_FILE = os.path.join(WORKING_DIR, 'Responses', f'List_{REG_ID}.json')
    HEADERS_FILE = os.path.join(WORKING_DIR, f'headers.json')
    
    KML_TEMPLATE_FILE = os.path.join(WORKING_DIR, 'kml_template.xml')
    with open (KML_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        KML_TEMPLATE = ''.join(f.readlines())

    GPX_TEMPLATE_FILE = os.path.join(WORKING_DIR, 'gpx_template.xml')
    with open (GPX_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        GPX_TEMPLATE = ''.join(f.readlines())

    