import boto3
import os
import sys
#import pandas as pd
#import matplotlib.pyplot as plt
import datetime

#Creating timestamp string to name bucket
d = datetime.datetime.now()
print('Hey whassup. The standard datetime is: {}'.format(d))
#Bucket name will include month, day, year, hour, minute, seconds
current_time = "{}{}{}{}{}{}".format(d.month, d.day, d.year, d.strftime("%I"), d.strftime("%M"), d.strftime("%S"))
print('Bam, the current time is {}'.format(current_time))

#Creating the S3 client
client = boto3.client('s3')

#Establishing the bucket name. Starting with my name and ending with the long timestamp
bucketName = 'omarfernandez{}'.format(current_time)

#Establishing the name of the file I want to upload and then delete
object_key = 'cousins.jpg'

#Creating S3 bucket
response = client.create_bucket(
    ACL='private',
    Bucket='{}'.format(bucketName),
    CreateBucketConfiguration={'LocationConstraint': 'us-west-1'},
    )

#Loading up the file
with open("cousins.jpg", 'rb') as f:
    data = f.read()

print('Uploading some data to {} with key: {}'.format(bucketName, object_key))

#Uploading file to S3 bucket
response = client.put_object(
    ACL='public-read',
    Body=data,
    Bucket=bucketName,
    Key=object_key
)

#Creating URL to for downloading
url = client.generate_presigned_url(
    'get_object', {'Bucket': bucketName, 'Key': object_key})
print('\nTry this URL in your browser to download the object:')
print(url)

#Pausing here so the user can observe the uploaded file in the S3 bucket
input("\nDone...Press enter to continue...")

#Using Resouce API, which provides resource objects that further abstract out the over-the-
#network API calls. Here, we'll instantiate and use 'bucket' or 'object' objects.
s3resource = boto3.resource('s3')

# Now, the bucket object
bucket = s3resource.Bucket(bucketName)

# Then, the object object
obj = bucket.Object(object_key)

#Show contents of bucket and object
print('Bucket name: {}'.format(bucket.name))
print('Object key: {}'.format(obj.key))
print('Object content length: {}'.format(obj.content_length))
print('Object body: {}'.format(obj.get()['Body'].read()))
print('Object last modified: {}'.format(obj.last_modified))

#Deleting the objects in the bucket
print('\nDeleting all objects in bucket {}.'.format(bucketName))
delete_responses = bucket.objects.delete()
for delete_response in delete_responses:
    for deleted in delete_response['Deleted']:
        print('\t Deleted: {}'.format(deleted['Key']))

#Deleting the bucket
print('\nDeleting the bucket.')
bucket.delete()

        
