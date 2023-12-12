FROM alpine:edge


RUN apk --update add --no-cache python3 py3-requests py3-pip openssl ca-certificates
RUN apk --update add --virtual build-dependencies python3-dev build-base wget git \
  && git clone https://github.com/maldevel/EmailHarvester.git
WORKDIR EmailHarvester

#COPY requirements.txt .
RUN python3 -m venv /path/to/venv
RUN . /path/to/venv/bin/activate
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "EmailHarvester.py"]
CMD ["-h"]
