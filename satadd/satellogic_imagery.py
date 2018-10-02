#Authenticate on telluric
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


def satfile(sensor,geometry,target):
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
    with open(os.path.join(home,'macro.csv'),'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["scene_id", "filename","download_url","location"], delimiter=',')
        writer.writeheader()
    with open(os.path.join(home,'micro.csv'),'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["scene_id", "filename","download_url","location"], delimiter=',')
        writer.writeheader()
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
                        filename=items['file_name']
                        itemurl=items['url']
                        locname=response['results'][0]['metadata']['location_requested_name']
                        files=itemurl.split('scenes/')[1].split('/rasters')[0]
                        bandname=itemurl.split('rasters/')[1].split('/download')[0]
                        if not os.path.exists(os.path.join(target,scene_id)):
                            os.mkdir(os.path.join(target,scene_id))
                        if not os.path.isfile(os.path.join(target,scene_id,bandname)):
                            print("Downloading "+str(os.path.join(target,scene_id,bandname)))
                            dest=os.path.join(target,scene_id,bandname)
                            url=itemurl
                            obj = SmartDL(url, dest)
                            obj.start()
                            path = obj.get_dest()
                        else:
                            print("File already exists skipping "+str(os.path.join(scene_id,bandname)))
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
                    for items in response['results'][0]['rasters']:
                        filename=items['file_name']
                        itemurl=items['url']
                        locname=response['results'][0]['metadata']['location_requested_name']
                        files=itemurl.split('scenes/')[1].split('/rasters')[0]
                        bandname=itemurl.split('rasters/')[1].split('/download')[0]
                        if not os.path.exists(os.path.join(target,scene_id)):
                            os.mkdir(os.path.join(target,scene_id))
                        if not os.path.isfile(os.path.join(target,scene_id,bandname)):
                            print("Downloading "+str(os.path.join(target,scene_id,bandname)))
                            dest=os.path.join(target,scene_id,bandname)
                            url=itemurl
                            obj = SmartDL(url, dest)
                            obj.start()
                            path = obj.get_dest()
                        else:
                            print("File already exists skipping "+str(os.path.join(bandname)))
            except Exception as e:
                print(e)

# satfile(sensor='micro',
#     geometry=r"C:\Users\samapriya\Downloads\westcoast.geojson",
#     target=r"C:\planet_demo\hyper")
