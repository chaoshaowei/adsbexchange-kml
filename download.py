import requests
import os
import json
import datetime
#-----------------------------
# Flags
#-----------------------------
DEBUG = False
FORCE_SEARCH = False
SAVE_RESPONSE = True

DIVIDE_LEG = True
DIVISOR_SECOND = 900

OUTPUT_TZ = datetime.timezone(datetime.timedelta(hours=-7))

OUTPUT_KML = True
OUTPUT_GPX = True

#-----------------------------
# directories
#-----------------------------


if __name__ == '__main__':
    #-----------------------------
    # Constants
    #-----------------------------
    REG_ID = 'N877BR'
    Y = 2022
    M = 9
    D = 20

    #-----------------------------
    # target url
    #-----------------------------
    HEX_URL_TEMPLATE = 'https://globe.adsbexchange.com/?icao=[HEX]'
    FLIGHT_URL_TEMPLATE = 'https://globe.adsbexchange.com/globe_history/[DATE]/traces/[HEX-2]/trace_full_[HEX].json'
    FLIGHT_URL_TEMPLATE2 = 'https://globe.adsbexchange.com/data/traces/[HEX-2]/trace_full_[HEX].json'
    REF_URL_TEMPLATE = 'https://globe.adsbexchange.com/?icao=[HEX]'

    #-----------------------------
    # directories
    #-----------------------------
    WORKING_DIR = os.path.dirname(os.path.realpath(__file__))

    RESPONSE1_FILE = os.path.join(WORKING_DIR, 'Responses', f'List_{REG_ID}.json')
    HEADERS_FILE = os.path.join(WORKING_DIR, f'headers.json')
    HEADERS2_FILE = os.path.join(WORKING_DIR, f'headers2.json')
    REG2HEX_FILE = os.path.join(WORKING_DIR, 'reg2hex.json')
    
    KML_TEMPLATE_FILE = os.path.join(WORKING_DIR, 'kml_template.xml')
    with open (KML_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        KML_TEMPLATE = ''.join(f.readlines())

    GPX_TEMPLATE_FILE = os.path.join(WORKING_DIR, 'gpx_template.xml')
    with open (GPX_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        GPX_TEMPLATE = ''.join(f.readlines())

    #-----------------------------
    # main
    #-----------------------------
    with open(REG2HEX_FILE, 'r', encoding='utf-8') as f1:
        reg2hex = json.load(f1)
    with open(HEADERS_FILE, 'r', encoding='utf-8') as f1:
        headers = json.load(f1)
    with open(HEADERS2_FILE, 'r', encoding='utf-8') as f1:
        headers2 = json.load(f1)

    try:
        HEX_ID = reg2hex[[entry["reg"] for entry in reg2hex].index(REG_ID)]['hex']
        print(f'Hex [{HEX_ID}] is for Reg [{REG_ID}]')
    except ValueError:
        print(f'Reg [{REG_ID}] not found, exit program')
        exit()

    s = requests.Session()

    #-----------------------------
    # Search Flight
    #-----------------------------
    def search_flight(hex_id: str, y: int, m: int, d: int):
        print(f"Searching Flight: {hex_id} for {y:04d}-{m:02d}-{d:02d}Z")
        date_str = f'{y:04d}/{m:02d}/{d:02d}'

        if not FORCE_SEARCH and False:
            print("  Will not be searched")
            return

        # Generate URL
        dtime = datetime.datetime.now(tz=datetime.timezone.utc)-datetime.datetime(year=Y, month=M, day=D, tzinfo=datetime.timezone.utc)
        hex_url = HEX_URL_TEMPLATE.replace('[HEX]', hex_id.lower())
        if dtime > datetime.timedelta(seconds=0) and dtime < datetime.timedelta(days=1):
            flight_url = FLIGHT_URL_TEMPLATE2.replace('[HEX]', hex_id.lower()).replace('[HEX-2]', hex_id[-2:].lower())
        else:
            flight_url = FLIGHT_URL_TEMPLATE.replace('[HEX]', hex_id.lower()).replace('[HEX-2]', hex_id[-2:].lower()).replace('[DATE]', date_str)
        print(f'    {flight_url}')

        # Getting Data
        r = s.get(hex_url, headers=headers)
        headers['referer'].replace('[HEX]', hex_id.lower())
        r = s.get(flight_url, headers=headers2)
        if r.status_code!=200:
            #print(r.text)
            if '404' in r.text:
                print(f'Error code 404')
                exit()
            if '403' in r.text:
                print(f'Error code 403')
                exit()
            print(f'Error code {r.statuscode}')
            exit()

        if SAVE_RESPONSE:
            # Saving Data
            os.makedirs(os.path.join(WORKING_DIR, 'Responses', REG_ID), exist_ok=True)
            RESPONSE_FILE = os.path.join(WORKING_DIR, 'Responses', REG_ID, f'{REG_ID}_{y:04d}-{m:02d}-{d:02d}Z.json')
            with open(RESPONSE_FILE, 'w', encoding='utf-8') as f:
                f.write(r.text)
        
        full_dict = json.loads(r.text)
        
        return full_dict

    def outputKML(flight_dict: dict):
        baseTimestamp = flight_dict["timestamp"]
        eventTime = datetime.datetime.fromtimestamp(baseTimestamp, tz=datetime.timezone.utc)

        reg = flight_dict['r']
        hex = flight_dict['icao']
        ref_url = REF_URL_TEMPLATE.replace('[HEX]',hex)

        track_list = flight_dict['trace']
        for point in track_list:
            try:
                float(point[3])
            except ValueError:
                point[3] = 0

        coords_str = '\n'.join([f'          {point[2]},{point[1]},{point[3]*0.3048}' for point in track_list])

        os.makedirs(os.path.join(WORKING_DIR, 'KMLs', reg), exist_ok=True)
        kml_file = os.path.join(WORKING_DIR, 'KMLs', reg, f'{reg}_{eventTime.strftime("%Y-%m-%dZ")}.kml')
        with open(kml_file, 'w', encoding='utf-8') as f:
            f.write(KML_TEMPLATE.replace('[COORDS]', coords_str).replace('[TRK_NAME]', f'Flight of {reg} at {eventTime.strftime("%Y-%m-%dZ")}').replace('[TRK_DSCRP]', f'{ref_url}'))
    
        if DIVIDE_LEG:
            slice_index_list = []
            last_sec = -DIVISOR_SECOND
            for idx, point in enumerate(track_list):
                if point[0] - last_sec >= DIVISOR_SECOND:
                    slice_index_list.append(idx)
                last_sec = point[0]
            slice_index_list.append(len(track_list))
            for idx in range(len(slice_index_list)-1):
                track_list = flight_dict['trace'][slice_index_list[idx]:slice_index_list[idx+1]]
                for point in track_list:
                    try:
                        float(point[3])
                    except ValueError:
                        point[3] = 0

                coords_str = '\n'.join([f'          {point[2]},{point[1]},{point[3]*0.3048}' for point in track_list])

                eventTimestamp = track_list[-1][0] + baseTimestamp
                eventTime = datetime.datetime.fromtimestamp(eventTimestamp, tz=datetime.timezone.utc)

                os.makedirs(os.path.join(WORKING_DIR, 'KMLs', reg), exist_ok=True)
                kml_file = os.path.join(WORKING_DIR, 'KMLs', reg, f'{reg}_{eventTime.astimezone(tz=OUTPUT_TZ).isoformat(timespec="minutes").replace(":","")}_D{DIVISOR_SECOND}.kml')
                with open(kml_file, 'w', encoding='utf-8') as f:
                    f.write(KML_TEMPLATE.replace('[COORDS]', coords_str).replace('[TRK_NAME]', f'Flight of {reg} at {eventTime.astimezone(tz=OUTPUT_TZ).isoformat(timespec="minutes")}').replace('[TRK_DSCRP]', f'{ref_url}'))

    def outputGPX(flight_dict: dict):
        baseTimestamp = flight_dict["timestamp"]
        eventTime = datetime.datetime.fromtimestamp(baseTimestamp, tz=datetime.timezone.utc)

        reg = flight_dict['r']
        hex = flight_dict['icao']
        ref_url = REF_URL_TEMPLATE.replace('[HEX]',hex)

        track_list = flight_dict['trace']

        coords_str = ''
        for point in track_list:
            try:
                float(point[3])
            except ValueError:
                point[3] = 0
            trkptTime = datetime.datetime.fromtimestamp(baseTimestamp+point[0], tz=datetime.timezone.utc)
            trkpt_time_str = trkptTime.isoformat()
            coords_str += f'      <trkpt lat="{point[1]}" lon="{point[2]}">\n        <ele>{point[3]*0.3048}</ele>\n        <time>{trkpt_time_str}</time>\n      </trkpt>\n'
        
        os.makedirs(os.path.join(WORKING_DIR, 'GPXs', reg), exist_ok=True)
        gpx_file = os.path.join(WORKING_DIR, 'GPXs', reg, f'{reg}_{eventTime.strftime("%Y-%m-%dZ")}.gpx')
        with open(gpx_file, 'w', encoding='utf-8') as f:
            f.write(GPX_TEMPLATE.replace('[COORDS]', coords_str).replace('[TIME]', eventTime.strftime("%Y-%m-%dZ")).replace('[TRK_NAME]', f'Flight of {reg} at {eventTime.strftime("%Y-%m-%dZ")}'))

        if DIVIDE_LEG:
            slice_index_list = []
            last_sec = -DIVISOR_SECOND
            for idx, point in enumerate(track_list):
                if point[0] - last_sec >= DIVISOR_SECOND:
                    slice_index_list.append(idx)
                last_sec = point[0]
            slice_index_list.append(len(track_list))
            for idx in range(len(slice_index_list)-1):
                track_list = flight_dict['trace'][slice_index_list[idx]:slice_index_list[idx+1]]
                coords_str = ''
                for point in track_list:
                    try:
                        float(point[3])
                    except ValueError:
                        point[3] = 0
                    trkptTime = datetime.datetime.fromtimestamp(baseTimestamp+point[0], tz=datetime.timezone.utc)
                    trkpt_time_str = trkptTime.isoformat()
                    coords_str += f'      <trkpt lat="{point[1]}" lon="{point[2]}">\n        <ele>{point[3]*0.3048}</ele>\n        <time>{trkpt_time_str}</time>\n      </trkpt>\n'
                
                os.makedirs(os.path.join(WORKING_DIR, 'GPXs', reg), exist_ok=True)
                gpx_file = os.path.join(WORKING_DIR, 'GPXs', reg, f'{reg}_{trkptTime.astimezone(tz=OUTPUT_TZ).isoformat(timespec="minutes").replace(":","")}_D{DIVISOR_SECOND}.gpx')
                with open(gpx_file, 'w', encoding='utf-8') as f:
                    f.write(GPX_TEMPLATE.replace('[COORDS]', coords_str).replace('[TIME]', trkptTime.astimezone(tz=OUTPUT_TZ).isoformat(timespec="minutes").replace(":","")).replace('[TRK_NAME]', f'Flight of {reg} at {trkptTime.astimezone(tz=OUTPUT_TZ).isoformat(timespec="minutes").replace(":","")}'))

    flight_dict = search_flight(HEX_ID, y=Y, m=M, d=D)
    if OUTPUT_KML:
        outputKML(flight_dict)
    if OUTPUT_GPX:
        outputGPX(flight_dict)

    exit()
    if RUN_MODE == SEARCH_FLIGHT_BY_FLIGHT_ID:
        ids = [FLIGHT_ID]
    elif RUN_MODE == SEARCH_FLIGHT_BY_REG or RUN_MODE == LIST_FLIGHT_BY_REG:
        ids = list_flights(reg_id=REG_ID)
    
    if RUN_MODE == SEARCH_FLIGHT_BY_REG or RUN_MODE == SEARCH_FLIGHT_BY_FLIGHT_ID:
        for flight_id in ids:
            flight_dict = search_flight(flight_id)
            if OUTPUT_KML:
                outputKML(flight_dict)
            if OUTPUT_GPX:
                outputGPX(flight_dict)
    
    exit()
