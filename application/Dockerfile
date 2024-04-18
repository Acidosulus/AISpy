FROM ubuntu:latest
RUN apt-get update -y
RUN apt install -y python3 python3-pip
COPY . /app
WORKDIR /app
RUN dir
RUN pip3 install -r /requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py", "flask"]