from band_calculator import BandCalculator
from aws_utils import get_bands_files, upload_to_s3, check_file_exists, s3_create_file, s3_delete_file
import os
from contextlib import contextmanager
from geoserver_api import add_coverage_store, add_layer

TEMP_DIR = 'temp'

@contextmanager
def create_temp_file(s3_name):
    s3_create_file(s3_name+"_started")
    yield
    s3_delete_file(s3_name+"_started")

def _process_and_upload(image_path, calculation='rgb'):
    b = BandCalculator(bands_dir=TEMP_DIR)
    s3_name = image_path.replace('/', '')+'/{}'.format(calculation)
    with create_temp_file(s3_name):
        if calculation == 'rgb':
            bands = [2, 3, 4]
            func = b.save_rgb
        elif calculation == 'ndvi':
            bands = [2, 8]
            func = b.save_ndvi

        if not os.path.exists(TEMP_DIR):
            os.mkdir(TEMP_DIR)
        get_bands_files(bands, dir_uri=image_path, output_dir=TEMP_DIR)
        temp_filepath = func()
        upload_to_s3(temp_filepath, s3_filename=s3_name)


def check_image_exists(image_path, type='rgb'):
    filename = image_path.replace('/', '') + "/" + type
    print("Checking if "+ filename + " exists")
    result =  check_file_exists(filename)
    print("Exists " if result else "Doesn't exist")
    return result

def add_new_rgb(image_path):
    _process_and_upload(image_path, calculation='rgb')

def add_new_ndvi(image_path):
    _process_and_upload(image_path, calculation='ndvi')



if __name__ == "__main__":
    add_new_rgb('tiles/34/U/DE/2016/5/23/0/')