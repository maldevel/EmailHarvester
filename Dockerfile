FROM alpine:edge


RUN apk --update add --no-cache python3 py3-requests py3-pip openssl ca-certificates
RUN apk --update add --virtual build-dependencies python3-dev build-base wget git \
  && git clone https://github.com/maldevel/EmailHarvester.git
WORKDIR EmailHarvester

#COPY email_harvester .
#COPY requirements.txt .
#COPY setup.py .
#COPY README.md .
#COPY LICENSE .
RUN python setup.py install
ENTRYPOINT ["email_harvester"]
CMD ["-h"]
