# FROM python:3.7
# LABEL maintainer="hoahh2201@gmail.com"
# ADD requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# ADD . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# EXPOSE 8080
# ENTRYPOINT ["python"]
# CMD ["app/main.py"]

FROM ubuntu:latest
# LABEL python_version=python3.7
RUN virtualenv --no-download /env -p python3.7

# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . /app/

#CMD gunicorn -b :$PORT main:app
ENTRYPOINT ["python"]
CMD ["app/main.py"]