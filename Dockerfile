FROM ubuntu:22.04
SHELL ["/bin/bash", "-c"]
EXPOSE 8000

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y --allow-unauthenticated wget gdal-bin libgdal-dev
RUN wget -nv https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3
RUN chmod +x /opt/miniconda3/bin/conda
ENV PATH="/opt/miniconda3/bin:$PATH"
RUN conda create -n moondiff; \
    source activate moondiff; \
    conda config --env --add channels conda-forge; \
    conda install django djangorestframework lerc gunicorn
RUN source activate moondiff; \
    pip install djangorangemiddleware gunicorn

WORKDIR /app
COPY . /app
ENTRYPOINT source activate moondiff; \
    python3 manage.py runserver 0.0.0.0:8000