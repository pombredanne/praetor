FROM daskdev/dask:latest

RUN conda install -c conda-forge prefect
COPY . /praetor
RUN pip install -r /praetor/requirements.txt
RUN pip install -e /praetor

