# DSA - Ch4Ep1
# Dockerfile introduction
#
# Objectives:
#   - airports file loader to mysql

# base form python3.7 image
FROM python:3.7.10-slim-buster

# adding env variables
ENV INPUT_FILE="/home/deb-airports.csv"

# set the working directory
WORKDIR /home

# add source files to the image
COPY * /home/

# install pip requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# add an ENTRYPOINT to execute the script on docker run
ENTRYPOINT ["python", "main.py"]
CMD [ ]
