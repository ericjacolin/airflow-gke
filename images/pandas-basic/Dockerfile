FROM continuumio/miniconda3:4.10.3

WORKDIR /opt/airflow/

# Install environment
COPY environments.yml environment.yml
RUN conda env update
