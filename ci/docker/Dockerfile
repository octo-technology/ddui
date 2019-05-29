FROM puckel/docker-airflow

ARG AIRFLOW_HOME=/usr/local/airflow

WORKDIR /usr/local/

COPY ./ ./ddui-plugin

USER root
WORKDIR /usr/local/ddui-plugin
RUN python setup.py install

WORKDIR /usr/local
RUN rm -fr /usr/local/ddui-plugin

USER airflow
RUN mkdir ${AIRFLOW_HOME}/plugins
RUN which ddui && ddui install
WORKDIR ${AIRFLOW_HOME}
