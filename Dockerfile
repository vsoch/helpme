FROM continuumio/miniconda3

# docker build -t vanessa/helpme .

RUN mkdir /code
ADD . /code
RUN /opt/conda/bin/pip install setuptools aiohttp && \
    /opt/conda/bin/pip install ipython && \
    /opt/conda/bin/pip install cchardet && \
    cd /code && /opt/conda/bin/python setup.py install

ENTRYPOINT ["helpme"]

ENV PATH /usr/local/bin:$PATH
LABEL maintainer vsochat@stanford.edu

WORKDIR /code
