# Language: dockerfile
# Path: Dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3-pip git
RUN git clone https://github.com/bhavyagoel/ServerStat.git
WORKDIR /ServerStat
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]