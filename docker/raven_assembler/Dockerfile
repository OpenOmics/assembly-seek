FROM ubuntu:22.04

RUN mkdir -p /opt2 && mkdir -p /data2
WORKDIR /opt2 

# Set time zone to US east coast 
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
       && echo $TZ > /etc/timezone

RUN apt-get update \
   && apt-get -y upgrade \
   && DEBIAN_FRONTEND=noninteractive apt-get install -y \
       build-essential \
       cmake \
       curl \
       gawk \
       git \
       gzip \
       g++ \
       libboost-dev \
       libcurl4-openssl-dev \
       libssl-dev \
       libxml2-dev \
       locales \
       # python/3.10.6
       python3 \
       python3-pip \
       samtools \
       wget \
       zlib1g-dev \
   && apt-get clean && apt-get purge \
   && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ENV CONDA_DIR /opt2/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt2/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# Set the locale
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

############### INSTALL ################
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN pip3 install --upgrade pip \
   && pip3 install matplotlib \
   && pip3 install numpy \
   && pip3 install pandas \
   && pip3 install scipy

RUN conda install -y --channel=defaults --channel=bioconda --channel=conda-forge raven-assembler

WORKDIR /opt2 

COPY Dockerfile /opt2
WORKDIR /data2
