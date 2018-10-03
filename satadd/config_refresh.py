import configparser
import os
import getpass
import requests
from os.path import expanduser
from gbdxtools import Interface
Config = configparser.ConfigParser()
try:
    config=configparser.ConfigParser()
    config.read(os.path.join(expanduser("~"),".satellogic-config"))
    url = 'https://auth.telluric.satellogic.com/api-token-auth/'
    uname=config.get('satellogic','user_name')
    passw=config.get('satellogic','user_password')
    payload = {'username':uname,'password':passw}
    r = requests.post(url, data=payload)
    if r.status_code != 200:
        raise ValueError("Telluric response error: %s" %r.text)
    telluric_token="JWT "+r.json()['token']
    with open(os.path.join(expanduser("~"),".satellogic-config"),'w') as cfgfile:
        Config.add_section('satellogic')
        Config.set('satellogic','user_name',uname)
        Config.set('satellogic','user_password', passw)
        Config.add_section('token')
        Config.set('token','access_token',telluric_token)
        Config.write(cfgfile)
        cfgfile.close()
    print('Satellogic Access token saved')
except Exception as e:
    print(e)

try:
    gbdx=Interface()
    print('GBDX Authenticated')
except Exception as e:
    print(e)
