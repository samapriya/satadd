import requests
import json
import time
import os
import csv
import sys
import configparser
from os.path import expanduser
from more_itertools import unique_everseen
os.chdir(os.path.dirname(os.path.realpath(__file__)))
home=os.path.dirname(os.path.realpath(__file__))


def metalist(sensor,geometry,target):
    with open(os.path.join(home,target),'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["id_no", "sun_elevation","gsd","location","satellite","date","system:time_start"], delimiter=',')
        writer.writeheader()
    if geometry !=None and os.path.isfile(geometry):
        footprint = {
        "type": "Polygon",
        "coordinates": []
            }
        f = open(geometry)
        for line in f:
            obj = json.loads(line)
            footprint['coordinates']=obj['features'][0]['geometry']['coordinates']
        params = {'footprint': json.dumps(footprint),'limit': 4000}
    else:
        params = {'limit': 4000}
    print("Getting token...")
    config=configparser.ConfigParser()
    config.read(os.path.join(expanduser("~"),".satellogic-config"))
    telluric_token=config.get('token','access_token')
    url = 'https://telluric.satellogic.com/v2/scenes/'
    header = { 'authorization' : telluric_token}
    print("Requesting scene...")
    r = requests.get(url, params=params,headers=header)
    if r.status_code != 200:
        raise ValueError("Telluric response error: %s" %r.text)
    response=r.json()
    print('')
    for scenes in response['results']:
        if sensor =='macro':
            try:
                if 'macro_cube' in scenes['scene_id']:
                    scene_id=scenes['scene_id']
                    params = {'scene_id': scene_id}
                    r = requests.get(url, params=params,headers=header)
                    response = r.json()
                    print('Processing '+str(response['results'][0]['scene_id']))
                    try:
                        sun_elevation=response['results'][0]['metadata']['sun_elevation']
                        gsd=30
                        location=response['results'][0]['metadata']['location_requested_name']
                        satellite=response['results'][0]['metadata']['product_metadata']['satellite']
                        date=response['results'][0]['metadata']['product_metadata']['date'].split('T')[0]
                        timestamp=response['results'][0]['metadata']['product_metadata']['timestamp']
                        #print(scene_id,sun_elevation,gsd,location,satellite,date,int(timestamp))
                        with open(target,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([scene_id, sun_elevation,gsd,location,satellite,date,int(timestamp)])
                        csvfile.close()
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
        elif sensor == 'micro':
            try:
                if 'micro' in scenes['scene_id']:
                    scene_id=scenes['scene_id']
                    params = {'scene_id': scene_id}
                    r = requests.get(url, params=params,headers=header)
                    response = r.json()
                    print('')
                    print('Processing '+str(response['results'][0]['scene_id']))
                    try:
                        sun_elevation=response['results'][0]['metadata']['sun_elevation']
                        gsd=1
                        location=response['results'][0]['metadata']['location_requested_name']
                        satellite=response['results'][0]['metadata']['product_metadata']['satellite']
                        date=response['results'][0]['metadata']['product_metadata']['date'].split('T')[0]
                        timestamp=response['results'][0]['metadata']['product_metadata']['timestamp']
                        #print(scene_id, sun_elevation,gsd,location,satellite,date,int(timestamp))
                        with open(target,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([scene_id, sun_elevation,gsd,location,satellite,date,int(timestamp)])
                        csvfile.close()
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
# satmeta(sensor='macro',geometry=r"C:\Users\samapriya\Downloads\world.geojson",
#     target=r"C:\planet_demo\hyper\meta.csv")
