# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11.5
SHELL ["/bin/bash", "-c"]

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1


# Set the working directory to /drf
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
WORKDIR /opt
COPY . /opt/ewm_backend
RUN ls .
# Install any needed packages specified in requirements.txt

RUN python -m venv venv
RUN source ./venv/bin/activate

#RUN pip install -r ewm_backend/requirements.txt
RUN pip install -r ewm_backend/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


VOLUME /opt

EXPOSE 8080

ENV ROOT /opt/ewm_backend/execution_devops

# CMD python $ROOT/manage.py makemigrations evm_bff && python $ROOT/manage.py migrate && python $ROOT/manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%"]
# CMD python $ROOT/manage.py makemigrations evm_bff && python $ROOT/manage.py migrate
# CMD ["/usr/local/bin/uwsgi", "--ini", "/opt/ewm_backend/uwsgi.ini"]
CMD python $ROOT/manage.py runserver 0.0.0.0:8000 --noreload

# docker build -t amr-registry.caas.intel.com/fia-cloud/ewm/ewm_backend:v0.0.1 .
# docker push amr-registry.caas.intel.com/fia-cloud/ewm/ewm_backend:v0.0.1