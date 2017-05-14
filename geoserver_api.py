import requests
from requests.auth import HTTPBasicAuth
import os


URL = 'http://ec2-35-156-13-22.eu-central-1.compute.amazonaws.com:8080/geoserver/rest/'
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


def add_coverage_store(ws, cs, path):
    headers = {'Content-Type': 'application/xml'}

    url = URL + 'workspaces/{ws}/coveragestores'.format(ws=ws)
    r = requests.post(url=url, headers=headers,
                  auth=auth, data='<coverageStore><name>{cs}</name><workspace>{ws}</workspace><type>GeoTIFF</type><url>{path}</url><enabled>true</enabled></coverageStore>'
                      .format(cs=cs, ws=ws, path=path))
    check_response(r)

def add_layer(ws, cs, name, title):
    headers = {'Content-Type': 'text/xml'}
    data = "<coverage><name>{name}</name><nativeName>{name}</nativeName><title>{title}</title></coverage>".format(cs=cs, name=name, title=title )
    url = URL + 'workspaces/{ws}/coveragestores/{cs}/coverages'.format(ws=ws, cs=cs)
    r = requests.post(url=url, headers=headers,
                  auth=auth, data=data)
    check_response(r)

if __name__ == "__main__":
    create_workspace('sentinel')
    add_coverage_store('sentinel', 'SentinelImage_2', path = 'file:///home/ubuntu/satellite-gis/rgb.tiff')
    add_layer(ws='sentinel', cs='SentinelImage_2', name="rgb", title="new_rgb")