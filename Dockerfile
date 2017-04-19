FROM ubuntu:16.04
RUN apt-get update -y -q && apt-get install -y -q locales python3-all python3-pip
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY . /app/
WORKDIR /app
RUN pip3 install -qr requirements.txt
EXPOSE 5000
CMD ["python3", "viaplay.py"]