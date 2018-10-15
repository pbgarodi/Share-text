# Share Text Web application


This application use to share the text with other user

    1. Receive the register request if user is not register,
    2. Once registation is done it will redirect to login page 
    3. Once user login then it will redirect to home page 
    4. In home page you can type text and Optionally you can encrypt text then hit Share buttom then it will generate shareable url

    5. Then you can share url with other user both user should be loged in
        If text encrypted you ned to shared decryption key as well with other user 

## python packages
- python==2.7 
- pip==8.1.1

## python dependencies
- Django==1.11.4
- djangorestframework==3.6.4
- pyjwt==1.6.4
- django-session-timeout==0.0.3 
- pycrypto==2.6.1


