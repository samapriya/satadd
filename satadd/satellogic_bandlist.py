import requests
import json
import time
import os
import csv
import sys
import configparser
from os.path import expanduser
from pySmartDL import SmartDL
os.chdir(os.path.dirname(os.path.realpath(__file__)))
home=os.path.dirname(os.path.realpath(__file__))


def bandlist(sensor,geometry,target):
    with open(os.path.join(target),'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["scene_id", "filename","download_url"], delimiter=',')
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
        print(r.status_code)
        raise ValueError("Telluric response error: %s" %r.text)
    response=r.json()
    for scenes in response['results']:
        if sensor =='macro':
            try:
                if 'macro_cube' in scenes['scene_id']:
                    scene_id=scenes['scene_id']
                    params = {'scene_id': scene_id}
                    r = requests.get(url, params=params,headers=header)
                    response = r.json()
                    print('')
                    print('Processing '+str(response['results'][0]['scene_id']))
                    for items in response['results'][0]['rasters']:
                        itemurl=items['url']
                        filename=items['file_name']
                        with open(os.path.join(target),'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([str(scene_id),str(filename),str(itemurl)])
                        csvfile.close()
            except Exception as e:
                print(e)
        elif sensor == 'micro':
            try:
                if 'micro' in scenes['scene_id']:
                    scene_id=scenes['scene_id']
                    params = {'scene_id': scene_id}
                    r = requests.get(url, params=params,headers=header)
                    if r.status_code==200:
                        response = r.json()
                        print('')
                        print('Processing '+str(response['results'][0]['scene_id']))
                        for items in response['results'][0]['rasters']:
                            itemurl=items['url']
                            filename=items['file_name']
                            with open(os.path.join(target),'a') as csvfile:
                                writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                                writer.writerow([str(scene_id),str(filename),str(itemurl)])
                            csvfile.close()
                    else:
                        print(r.status_code)
            except Exception as e:
                print(e)

# bandlist(sensor='macro',
#     geometry=r"C:\Users\samapriya\Downloads\westcoast.geojson",
#     target=r"C:\planet_demo\hyper\macrout.csv")
