import boto3
import botocore
import json
from collections import namedtuple
import os
from timer import Timer

Image = namedtuple("AWSImageData", ['prefix', 'clouds', 'data_percentage', 'date'])

sentinel_bucket_name = 'sentinel-s2-l1c'
BUCKET ='s2processedimages'
prefix = 'tiles/34/U/CF/' # prefix for Pomeranian district

s3 = boto3.resource('s3', region_name='eu-central-1')
b = s3.Bucket(sentinel_bucket_name)

client = boto3.client('s3', region_name='eu-central-1')#,
#                      config=botocore.client.Config(signature_version=botocore.UNSIGNED))

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
        #img_dir = os.path.join(output_dir, dir_uri.replace('/',''))
        img_dir=output_dir
        with Timer('{} download'.format(band_filename)):
            client.download_file(sentinel_bucket_name, file_key, os.path.join(output_dir, band_filename))
    return img_dir

def s3_create_file(filename, data=b''):
    client.put_object(Key=filename, Bucket=BUCKET, Body=data)

def s3_delete_file(key):
    client.delete_object(Key=key, Bucket=BUCKET)

def s3_download_file(key, output_filepath):
    client.download_file(Key=key, Bucket=BUCKET, Filename=output_filepath)
    return True

def upload_to_s3(filepath, s3_filename = None, bucket='s2processedimages'):
    if s3_filename is None:
        s3_filename = filepath
    client.upload_file(filepath, bucket, s3_filename)
    print(s3_filename + " uploaded to S3")

def check_file_exists(filepath, bucket='s2processedimages'):
    try:
        client.head_object(Bucket=bucket, Key=filepath)
        return True
    except:
        return False

if __name__ == '__main__':
    print(check_file_exists('test.txt'))
