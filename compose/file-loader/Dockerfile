FROM python:3.7.10-slim-buster

# adding env variables
ENV INPUT_FILE="/home/deb-airports.csv"
# set the working directory
WORKDIR /home
# add source files to the image
COPY * /home/
# install pip requirements
RUN pip3 install -r requirements.txt

# execute the script on docker run
CMD ["python", "main.py"]
