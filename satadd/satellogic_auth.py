import configparser
import os
import getpass
import requests
from os.path import expanduser
Config = configparser.ConfigParser()
username= raw_input("Enter your username: ")
password=getpass.getpass('Enter your password: ')
url = 'https://auth.telluric.satellogic.com/api-token-auth/'
payload = {'username':username,'password':password}
print("Getting token...")
r = requests.post(url, data=payload)
if r.status_code != 200:
    raise ValueError("Telluric response error: %s" %r.text)
telluric_token="JWT "+r.json()['token']
with open(os.path.join(expanduser("~"),".satellogic-config"),'w') as cfgfile:
    Config.add_section('satellogic')
    Config.set('satellogic','user_name',username)
    Config.set('satellogic','user_password', password)
    Config.add_section('token')
    Config.set('token','access_token',telluric_token)
    Config.write(cfgfile)
    cfgfile.close()
print('Access token saved')
