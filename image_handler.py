
from __future__ import print_function

import logging
import uuid
import boto3
from PIL import Image
import PIL.Image

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_RAW_BUCKET = "lambda-image-raw"
S3_RESULT_BUCKET = ""

s3_client = boto3.client('s3')

def image_handler(event, context):
    logger.info('got event{}'.format(event))

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}/{}'.format(uuid.uuid4, key)
        upload_path = '/tmp/resized-{}'.format(key)

        s3_client.download_file(bucket, key, download_path)
        process_image(download_path, upload_path)

        logger.info('download path : %s ', download_path)
        logger.info('upload path : %s ', upload_path)

        s3_client.upload_file(upload_path, '{}resized'.format(bucket), key)

    logger.error('something went wrong')
    return 'Halo World from lambda'



def process_image(downloaded_path, resized_path):
    with Image.open(downloaded_path) as im:
       im.thumbnail(tuple(x/2 for x in im.size))
       im.save(resized_path)



def main():
    image_handler(None, None)
    process_image("/Users/sjoshi/1522573043274.jpg")


if __name__ == "__main__": main()