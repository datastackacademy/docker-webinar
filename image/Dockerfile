# Dockerfile introduction
#
# Objectives:
#   - Create a basic image from a python3.7 base
#   - Add data files and python scripts
#   - Run the script

# base form python3.7 image
# the first line of dockerfile must always set the base image
# be careful about which image you choose.
# for python the "slim" or "buster" images are the BEST. This will resolve a lot of your issues in 
# the future. Please refer to:
#   https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:3.7.10-slim-buster

# set the working directory
# all other paths following this command (like COPY and CMD) can be relative to this path
WORKDIR /home

# add source files to the image
# COPY adds a file from host directory to the image
# syntax:
#   COPY <src> <dest>
#   where <src> is name of files or directories on the host machine. You can use wildcards here!
#   and <dest> is the directory on the docker image being built. This path can be relative to WORKDIR above
COPY names.txt main.py ./

# run the script when image executes
# every dockerfile can have ONLY ONE CMD line
# this the default command that runs when you execute `docker run`
CMD ["python", "main.py"]
