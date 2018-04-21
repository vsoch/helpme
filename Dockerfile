FROM continuumio/miniconda3

# docker build -t vanessa/helpme .

RUN mkdir /code
ADD . /code
RUN /opt/conda/bin/pip install setuptools && \
    /opt/conda/bin/pip install pip --upgrade && \
    /opt/conda/bin/pip install -r requirements.txt && \
    cd /code && /opt/conda/bin/python setup.py install

ENTRYPOINT ["helpme"]

ENV PATH /usr/local/bin:$PATH
LABEL maintainer vsochat@stanford.edu

WORKDIR /code
