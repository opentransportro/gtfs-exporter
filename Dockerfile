FROM opentransport/pfaedle
MAINTAINER OpenTransport version: 0.1

ENV WORK=/opt/gtfs-exporter
WORKDIR ${WORK}
RUN mkdir -p ${WORK}

RUN apt update && apt install -y python3 python3-pip
RUN rm -rf /var/lib/apt/lists/*
ADD . ${WORK}
RUN cd ${WORK} && pip3 install . && python3 setup.py install
