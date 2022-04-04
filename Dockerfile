FROM python:3.9

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        wget
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y zip unzip build-essential libsnappy-dev zlib1g-dev libbz2-dev \
    libgflags-dev liblz4-dev libzstd-dev \
    librocksdb-dev

WORKDIR /example-api

COPY . /example-api

RUN pip3 install -r requirements.txt

CMD python3 main.py