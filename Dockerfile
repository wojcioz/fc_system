FROM rustembedded/cross:armv7-unknown-linux-gnueabihf

RUN apt-get update  
RUN apt-get install -y libraspberrypi-dev