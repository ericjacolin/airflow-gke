FROM continuumio/miniconda3:4.10.3

WORKDIR /opt/airflow/

# install environment
COPY ./environments/requirements.txt requirements.txt
RUN conda env create -f environment.yml
RUN . /root/.bashrc && \
    conda init bash && \
    conda activate papermill && \
    pip install -r requirements.txt && \
    python -m ipykernel install --user --name=papermill

RUN pip install ipykernel papermill

COPY ./notebooks /opt/airflow/notebooks
COPY ./output /opt/airflow/output
COPY ./data /opt/airflow/data

# CMD ["papermill", "--help-notebook", "/opt/airflow/notebooks/papermill.test.ipynb"]
