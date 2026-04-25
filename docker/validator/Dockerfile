FROM ubuntu:22.04

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglu1-mesa && rm -rf /var/lib/apt/lists/*

# Copy AFSIM runtime into image.
COPY ./afsim_bin /opt/afsim
ENV PATH="/opt/afsim:${PATH}"

WORKDIR /sandbox
