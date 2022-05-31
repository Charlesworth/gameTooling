from datetime import datetime
from typing import NamedTuple
import json
import os

print('*** S3 BACKUP UTIL ***')

######################## Parse the config options

class Conf(NamedTuple):
    target_dir: str
    bucket_name: str
    r2_endpoint_url: str
    r2_access_key_id: str
    r2_secret_access_key: str
    b2_endpoint_url: str
    b2_access_key_id: str
    b2_secret_access_key: str

def read_json_conf() -> Conf:
    f = open('conf.json', "r")
    data = json.loads(f.read())
    f.close()
    return Conf(
        target_dir=data['target_dir'],
        bucket_name=data['bucket_name'],
        r2_endpoint_url=data['r2_endpoint_url'],
        r2_access_key_id=data['r2_access_key_id'],
        r2_secret_access_key=data['r2_secret_access_key'],
        b2_endpoint_url=data['b2_endpoint_url'],
        b2_access_key_id=data['b2_access_key_id'],
        b2_secret_access_key=data['b2_secret_access_key']
    )

conf = read_json_conf()

######################## Zip the directories

import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))

def zipit(dir_list, zip_name):
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for dir in dir_list:
        zipdir(dir, zipf)
    zipf.close()

date_today = datetime.today().strftime('%Y-%m-%d-%H%M')
zip_output_file_name = f'bgaBackup_{date_today}.zip'

print(f'{datetime.now().strftime("%H:%M:%S")} zipping "Assets" and "ProjectSettings" from target directory "{conf.target_dir}"')
zipit([f'{conf.target_dir}/Assets', f'{conf.target_dir}/ProjectSettings'], zip_output_file_name)
print(f'{datetime.now().strftime("%H:%M:%S")} finished zip')

######################## Upload to r2 and b2

import boto3
import logging
from botocore.exceptions import ClientError
from botocore.config import Config

def upload_file(file_name, bucket, s3_client, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

print(f'{datetime.now().strftime("%H:%M:%S")} starting r2 s3 upload')
r2_s3_client = boto3.client('s3',
  endpoint_url = conf.r2_endpoint_url,
  aws_access_key_id = conf.r2_access_key_id,
  aws_secret_access_key = conf.r2_secret_access_key
)
r2_upload_success = upload_file(zip_output_file_name, conf.bucket_name, r2_s3_client)
print(f'{datetime.now().strftime("%H:%M:%S")} r2 s3 upload {"SUCCESS" if r2_upload_success else "ERROR"}')

print(f'{datetime.now().strftime("%H:%M:%S")} starting b2 s3 upload')
b2_s3_client = boto3.client(service_name='s3',
    endpoint_url = conf.b2_endpoint_url,
    aws_access_key_id = conf.b2_access_key_id,
    aws_secret_access_key = conf.b2_secret_access_key,
    config=Config(signature_version='s3v4')
)
b2_upload_success = upload_file(zip_output_file_name, conf.bucket_name, b2_s3_client)
print(f'{datetime.now().strftime("%H:%M:%S")} r2 s3 upload {"SUCCESS" if b2_upload_success else "ERROR"}')

######################## Clean up .zip

print(f'{datetime.now().strftime("%H:%M:%S")} cleaning .zip')
os.remove(zip_output_file_name)

print(f'{datetime.now().strftime("%H:%M:%S")} finished')
