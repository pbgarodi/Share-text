# This will pull ubuntu image from docker hub as base docker image
FROM python:latest

# create root directory for our project in the container
RUN mkdir /share_text_app

# Copy all containt to share_text_app dir
COPY . /share_text_app/

# Set the working directory to /share_text_app
WORKDIR /share_text_app

# Install all requirement
RUN pip install -r requirements.txt

CMD python3 manage.py runserver 0.0.0.0:8000