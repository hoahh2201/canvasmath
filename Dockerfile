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

FROM gcr.io/google-appengine/python
LABEL python_version=python3.7
RUN virtualenv --no-download /env -p python3.7

# Various Python and C/build deps
RUN apt-get update && apt-get install -y \ 
    wget \
    build-essential \ 
    cmake \ 
    git \
    unzip \ 
    pkg-config \
    python-dev \ 
    python-opencv \ 
    libopencv-dev \ 
    libav-tools  \ 
    libjpeg-dev \ 
    libpng-dev \ 
    libtiff-dev \ 
    libjasper-dev \ 
    libgtk2.0-dev \ 
    python-numpy \ 
    python-pycurl \ 
    libatlas-base-dev \
    gfortran \
    webp \ 
    python-opencv \ 
    qt5-default \
    libvtk6-dev \ 
    zlib1g-dev 

# Install Open CV - Warning, this takes absolutely forever
RUN mkdir -p ~/opencv cd ~/opencv && \
    wget https://github.com/opencv/opencv/archive/3.0.0.zip && \
    unzip 3.0.0.zip && \
    rm 3.0.0.zip && \
    mv opencv-3.0.0 OpenCV && \
    cd OpenCV && \
    mkdir build && \ 
    cd build && \
    cmake \
    -DWITH_QT=ON \ 
    -DWITH_OPENGL=ON \ 
    -DFORCE_VTK=ON \
    -DWITH_TBB=ON \
    -DWITH_GDAL=ON \
    -DWITH_XINE=ON \
    -DBUILD_EXAMPLES=ON .. && \
    make -j4 && \
    make install && \ 
    ldconfig

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