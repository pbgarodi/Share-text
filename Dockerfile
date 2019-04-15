# This will pull ubuntu image from docker hub as base docker image
FROM ubuntu
# Author name
MAINTAINER Pravin Garodi (pbgarodi@gmail.com)

# Update base image
RUN apt-get update

# system-level packages.
RUN apt-get install -y python-pip
# sudo apt install

# create root directory for our project in the container
RUN mkdir /share_text_app

# Copy all containt to share_text_app dir
ADD . /share_text_app/

# Set the working directory to /share_text_app
WORKDIR /share_text_app

# Install all requirement
RUN pip install -r requirements.txt
