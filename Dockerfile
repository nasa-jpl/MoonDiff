FROM ubuntu:22.04
SHELL ["/bin/bash", "-c"]
EXPOSE 8000

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y --allow-unauthenticated wget
RUN wget -nv https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3
RUN chmod +x /opt/miniconda3/bin/conda
ENV PATH="/opt/miniconda3/bin:$PATH"
RUN conda create -n moondiff; \
    source activate moondiff; \
    conda install libspatialite gdal django poppler sqlite lerc gunicorn pyyaml; \
    pip install djangorestframework whitenoise dj-rest-auth[with_social] # These are not in conda and conda-forge was causing dep issues

WORKDIR /app
COPY . /app
ENTRYPOINT /app/entrypoint.sh
