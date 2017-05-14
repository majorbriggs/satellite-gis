from aws_utils import s3_download_file
from geoserver_api import add_coverage_store, add_layer
import os

GEOSERVER_DATA_DIR = "/home/ubuntu/satellite-gis/"
#GEOSERVER_DATA_DIR = "/home/piotrek/data/"

def download_from_s3_and_add_layer(image_key):
    data_store_name = image_key.replace('/', '')
    filepath = GEOSERVER_DATA_DIR + data_store_name
    s3_download_file(image_key, filepath)
    data_source_path = "file://" + filepath
    add_coverage_store('sentinel', data_store_name, path=data_source_path)
    add_layer(ws='sentinel', cs=data_store_name, name=data_store_name, title=data_store_name)
    return True
