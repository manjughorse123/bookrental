from rest_framework_jwt.settings import api_settings

def generate_jwt_token(user, data):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    payload['username'] = payload['username'].raw_input
    payload['phone_number'] = payload['phone_number'].raw_input
    token = jwt_encode_handler(payload)
    data['token'] = token
    return data

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import requests
import boto3


def upload_file(s3_image_filename, file_url):

    s3_image_filename = s3_image_filename.replace(' ','')
    s3 = boto3.resource('s3')
    bucket_name_to_upload_image_to = 'eatburp-img'
    # s3_image_filename = 'test_s3_image.png'
    good_to_go = False


    for bucket in s3.buckets.all():
        if bucket.name == bucket_name_to_upload_image_to:
            print('Good to go. Found the bucket to upload the image into.')
            good_to_go = True

    if not good_to_go:
        print('Not seeing your s3 bucket, might want to double check permissions in IAM')

    try:
        req_for_image = requests.get(file_url, stream=True)
        file_object_from_req = req_for_image.raw
        req_data = file_object_from_req.read()
    except Exception as e:
        return None

    s3.Bucket(bucket_name_to_upload_image_to).put_object(Key=s3_image_filename, Body=req_data)
    return 'https://s3.ap-south-1.amazonaws.com/eatburp-img/' + s3_image_filename


from twilio.rest import Client
from twilio.jwt.client import ClientCapabilityToken


class TwilioAPI:

    def __init__(self):
        self.AccountId = 'AC5d2600db1b5ec0128255d6a3fecd9980'
        self.AuthToken = "bfb577fc883927f5636e648da22d01eb"
        self.SubAccountId = None

    def get_client(self):
        return Client(self.AccountId, self.AuthToken)

    def get_client_capability_token(self):
        capability = ClientCapabilityToken(self.AccountId, self.AuthToken)
        capability.allow_client_incoming('APf2af8000083f42fca4f2789a1d9a7867')
        capability.allow_client_outgoing('APf2af8000083f42fca4f2789a1d9a7867')
        return capability.to_jwt()

    def send_message(self, to_number, from_number, msg):
        try:
            response = self.get_client().messages.create(
                to_number,
                from_=from_number,
                body=msg,
            )
        except Exception as e:
            print(e)
            return {'status': False}
        return {'status': True, 'data':response.status}