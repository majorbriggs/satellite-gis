import requests
from requests.auth import HTTPBasicAuth
import os


URL = 'http://ec2-35-158-55-99.eu-central-1.compute.amazonaws.com:8080/geoserver/rest/'
headers = {'Content-Type': 'text/xml'}
auth = HTTPBasicAuth(username=os.getenv('GEOSERVER_USERNAME'), password='DaleCooper')

def check_response(r):
    if r.status_code == 201:
        return True
    else:
        print('Request failed\n{} {}'.format(r.status_code, r.content))


def create_workspace(name):
    url = URL + 'workspaces'

    r = requests.post(url=url, headers=headers,
                      auth=auth, data='<workspace><name>{}</name></workspace>'.format(name))
    check_response(r)


def add_coverage_store(ws, cs):
    headers = {'Content-Type': 'application/xml'}

    url = URL + 'workspaces/{ws}/coveragestores'.format(ws=ws)
    r = requests.post(url=url, headers=headers,
                  auth=auth, data='<coverageStore><name>{cs}</name><workspace>{ws}</workspace><type>GeoTIFF</type><enabled>true</enabled></coverageStore>'.format(cs=cs, ws=ws))
    check_response(r)
create_workspace('sentinel')
add_coverage_store('sentinel', 'SentinelImage_1')