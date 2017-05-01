import boto3
import botocore
import json
from collections import namedtuple
import os

Image = namedtuple("AWSImageData", ['prefix', 'clouds', 'data_percentage', 'date'])

sentinel_bucket_name = 'sentinel-s2-l1c'

prefix = 'tiles/34/U/CF/' # prefix for Pomeranian district

s3 = boto3.resource('s3', region_name='eu-central-1')
b = s3.Bucket(sentinel_bucket_name)

client = boto3.client('s3', region_name='eu-central-1',
                      config=botocore.client.Config(signature_version=botocore.UNSIGNED))

def get_images_data(prefix=prefix):
    result = client.list_objects(Bucket=sentinel_bucket_name,
                                 Prefix=prefix,
                                 Delimiter='/'
                                 )
    prefixes = result.get('CommonPrefixes') or []
    for o in prefixes:
        new_prefix = o.get('Prefix')

        if len(new_prefix.split('/')) == 9:
            j = b.Object(new_prefix + 'tileInfo.json').get()['Body']
            tile_info = json.loads(j.read().decode('utf-8'))
            yield Image(prefix=new_prefix,
                        clouds=tile_info['cloudyPixelPercentage'],
                        data_percentage=tile_info['dataCoveragePercentage'],
                        date=tile_info['timestamp'].split('T')[0])
        for i in get_images_data(prefix=new_prefix):
            yield i



def get_preview_from_sentinel(dir_uri, output_dir):
    filename = 'preview.jpg'
    img_dir = os.path.join(output_dir, dir_uri.replace('/', ''))
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
        client.download_file(sentinel_bucket_name, dir_uri+'preview.jpg', os.path.join(img_dir, filename))
    return filename

def get_bands_files(bands, dir_uri, output_dir):
    for band in bands:
        band_filename = "B{:>02}.jp2".format(band)
        file_key = dir_uri + band_filename
        img_dir = os.path.join(output_dir, dir_uri.replace('/',''))
        os.mkdir(img_dir)
        client.download_file(sentinel_bucket_name, file_key, os.path.join(output_dir, img_dir, band_filename))


if __name__ == '__main__':
    get_preview_from_sentinel('tiles/34/U/CF/2015/10/6/0/', '.')