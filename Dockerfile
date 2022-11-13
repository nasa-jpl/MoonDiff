FROM ubuntu:22.04
SHELL ["/bin/bash", "-c"]
EXPOSE 8000

ENV DEBIAN_FRONTEND=noninteractive

RUN env > myenv.txt
RUN apt-get update
RUN apt-get install -y --allow-unauthenticated wget
RUN wget -nv https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3
RUN chmod +x /opt/miniconda3/bin/conda
ENV PATH="/opt/miniconda3/bin:$PATH"
RUN conda create -n moondiff; \
    source activate moondiff; \
    conda install libspatialite gdal django poppler sqlite lerc gunicorn; \
    pip install djangorestframework

WORKDIR /app
COPY . /app
ENTRYPOINT /app/entrypoint.sh
