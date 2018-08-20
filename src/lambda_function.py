import boto3
import zipfile
from io import BytesIO
from PIL import Image

#-------- global variables -------
images_bucket = 'batch-images-bucket'
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']
    image_list = event['image_list']

    # Download and save the zip to tmp storage
    s3_client.download_file(bucket, key,  '/tmp/file.zip')

    try:
        # unzip our image file
        images_zip = zipfile.ZipFile('/tmp/file.zip')

        # Iterate through our list of image names
        for image_name in image_list:
            data = images_zip.read(image_name)
            image = Image.open(BytesIO(data))
            buffer = BytesIO()
            image.save(buffer, 'png')
            buffer.seek(0)

            # Uploading the image
            obj = s3.Object(bucket_name=images_bucket, key=image_name.replace('.tif', '.png'))
            obj.put(Body=buffer, ContentType='image/png', ServerSideEncryption='AES256')

    except Exception as e:
        print(e)
        print('Error uploading images for zip file {} images {}.'.format(image_list, image_list))
        raise e
