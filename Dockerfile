From ubuntu:focal
COPY install.sh ./
RUN DEBIAN_FRONTEND=noninteractive ./install.sh