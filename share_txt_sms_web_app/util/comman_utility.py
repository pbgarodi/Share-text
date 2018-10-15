import time
import datetime
import os
import time
# Project related dependencies
import jwt
from Share_Text import settings
from Crypto.Cipher import AES
import base64
from base64 import b64encode
import os


class CommonUtility: 
    
    BLOCK_SIZE = 16
    PADDING = ')'
    
    # This method will generate token and return dictionary
    @staticmethod
    def generate_token(message_id,secret_key,encrypt_flag=False,):
        """
        this method will generate jwt token 
        @params:
           messagee_id =  id of massage which we are going to share 
        @returns- jwt token
        """
        date_1 = datetime.datetime.utcnow()
        end_date = date_1 + datetime.timedelta(days=7) 
        payload = {
        'message_id': message_id,
        'encrypt_flag':encrypt_flag,
        'exp' : end_date
        }
        jwt_token = {'token': (jwt.encode(payload, secret_key ,algorithm='HS256')).decode("utf-8")}

        return jwt_token

    @staticmethod
    def decode_token(token, secrect_key):
        """
        This method will decode jwt token 
        @params:
           token = token to be decode  
        @returns- dictionary 
        """
        token_data = decodedPayload = jwt.decode(token,secrect_key,algorithm='HS256')
        return token_data

    @staticmethod
    def encrypt(message):
        pad = lambda s: s + (CommonUtility.BLOCK_SIZE - len(s) % CommonUtility.BLOCK_SIZE) *CommonUtility.PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        secret = os.urandom(CommonUtility.BLOCK_SIZE)
        key = b64encode(secret).decode('utf-8')
        cipher = AES.new(key)
        encoded = EncodeAES(cipher, message)
        #print('encrypted data:',encoded)
        
        #print('key:',secret)
        return encoded,key
    @staticmethod
    def decrypt(secret,encoded_message):
        decoded_message = None
        try:
            DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(CommonUtility.PADDING)
            cipher = AES.new(secret)
            decoded_message = DecodeAES(cipher, encoded_message)
        except Exception as e:
            pass
        return decoded_message
