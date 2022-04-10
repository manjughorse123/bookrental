from rest_framework_jwt.settings import api_settings
from user.models import *
import jwt

def generate_jwt_token(user, data):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    data['token'] = token
    return data

def generate_jwt_token_only(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    
    return token


def verify_token(token):
    try:
        # token = request
        # import pdb;pdb.set_trace()
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        response = {}
        payload = None
        try:
            payload = jwt_decode_handler(token)            
            response['payload'] = payload
            try:
                user = User.objects.get(id=payload['user_id'])
                # check_pwd = user.check_password(payload['password'])
                if user:
                    payload = 'Verified'
                    response['payload'] = user
                    response['status'] = True
                else:
                    payload = "Wrong Credentials are provided"
                    response['status'] = False
            except:
                payload = "Wrong Credentials are provided"
                response['status'] = False
        except jwt.ExpiredSignature:
            payload = 'Signature has expired.'
            response['status'] = False
        except jwt.DecodeError:
            payload = 'Error decoding signature.'
            response['status'] = False
        response['msg'] = payload
        return response
    except:
        payload = 'Token is not provided.'
        return {'status':False, 'msg':payload}
