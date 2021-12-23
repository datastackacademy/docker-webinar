# docker-webinar

Data Stack Academy Webinar Series - Intro to Docker 

# Docker-cli

```bash
# pull busybox
docker pull busybox

# list your images
docker images

# run busybox
docker run busybox echo "hello from docker"

# using docker ps
docker ps
docker ps -a

# another way to run without lingering images
docker run --rm busybox echo "hello from docker"

# remove lingering images
docker system prune -a

# running with interactive shell
docker run -it --rm --name terminal busybox
# open another terminal and execute
docker exec -it terminal /bin/sh

# working with volumes
docker run --rm -it -v data:/data busybox
echo "goodbye blue skies" > /testfile.txt
exit

docker volume ls
docker volume inspect data
docker volume rm data

# attaching local dirs as volume
docker run --rm -it -v $(pwd)/data:/data busybox

# working with ports and volumes
docker pull nginx
docker run -d --name nginx-server -v $(pwd)/data:/usr/share/nginx/html:ro -p 8080:80 nginx

```

# Dockerfile

Building a docker image:

```bash
cd image

# check out the image code and Dockerfile
code .

# build and run the image
docker build -t first-image:latest .

docker run --rm first-image:latest
```

# Docker-compose

```bash
cd compose

# run everything!
docker-compose up

# test the api
curl --location --request GET 'http://172.18.0.3:5000/?iata=PDX' | python3 -m json.tool
```
