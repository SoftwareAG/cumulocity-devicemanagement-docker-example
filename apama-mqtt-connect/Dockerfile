ARG SAG_HOME=/opt/softwareag
ARG ACCE_VERSION=10.5.3.2
ARG ACCE_LIBRARY_VERSION=10.5

# Docker Mulit-stage build

# First our builder image that does the download of Apama Core (some base images have to have curl added here)
FROM balenalib/rpi-raspbian:jessie as acce_build
ARG SAG_HOME
ARG ACCE_VERSION

# Get/download the compressed archive of Apama Core Community Edition, and unzip it

RUN \
    ACCE_BASE_URL=https://downloads.apamacommunity.com/apama-core/${ACCE_VERSION} && \
    ACCE_TGZ_FILE=apama_core_${ACCE_VERSION}_armv7_linux.tar.gz && \
    ACCE_INSTALL_FOLDER=${SAG_HOME} && \
    mkdir $ACCE_INSTALL_FOLDER && \
    curl -s $ACCE_BASE_URL/$ACCE_TGZ_FILE | tar -xvz -C $ACCE_INSTALL_FOLDER

COPY ./catalogs ${SAG_HOME}/Apama/catalogs

# Now make the real image (for some images that does not include the extra 14MB of curl and dependencies)
# next == Buster (testing)
# 9 == Stretch (current stable)
# 8 == Jessie (obsolete stable) ** used here **
# 7 == Wheezy (obsolete stable)
# 6 == Squeeze (obsolete stable)
FROM balenalib/rpi-raspbian:jessie
ARG SAG_HOME
ARG APAMA_HOME=${SAG_HOME}/Apama
ARG APAMA_WORK=/apama_work
ARG ACCE_VERSION
ARG ACCE_LIBRARY_VERSION
ARG APAMA_PROJECT=/Project_deployed

LABEL \
    name="Apama Core Community Edition" \
    arch="armv7hf" \
    base="balenalib/rpi-raspbian:jessie" \
    maintainer="Kev Palfreyman (@kpalf)" \
    build-date="20190428" \
    version=${ACCE_VERSION}

# Set the shell and create user identical to the official SAG images
SHELL ["/bin/bash", "-c"]
RUN groupadd -g 1724 sagadmin && useradd -d /opt/softwareag --no-create-home -g 1724 -u 1724 sagadmin

# Copy the unzipped Apama Core Community Edition from the "acce_build" interim image, with correct user:group
COPY --from=acce_build --chown=sagadmin:sagadmin ${SAG_HOME} ${SAG_HOME}
COPY --chown=1724:1724 . ${APAMA_WORK}/Project_deployed

# Set environment variables inside the image
ENV \
    SAG_HOME=${SAG_HOME} \
    APAMA_HOME=${APAMA_HOME} \
    APAMA_WORK=${APAMA_WORK} \
    APAMA_PROJECT=/Project_deployed \
    APAMA_LIBRARY_VERSION=${ACCE_LIBRARY_VERSION} \
    APAMA_PLATFORM=armv7_linux \
    PATH=${APAMA_HOME}/bin:$PATH \
    LD_LIBRARY_PATH=${APAMA_HOME}/lib:${APAMA_WORK}/lib:$LD_LIBRARY_PATH \
    PYTHONPATH=${APAMA_HOME}/third_party/python/lib/python3.6/site-packages

RUN ldconfig

WORKDIR ${APAMA_WORK}
RUN chown sagadmin:sagadmin ${APAMA_WORK}

# Standard server port for the correlator CEP/Streaming-Analytics engine
EXPOSE 15903

# Primary binary for the CEP/Streaming-Analytics engine, but the image also
# contains the standard tools such as engine_inject, engine_send, etc
USER sagadmin:sagadmin
RUN if [ -e ${APAMA_WORK}/Project/TypeRepository ]; then rm -rf ${SAG_HOME}/common/DigitalEventServices/TypeRepository; cp -a ${APAMA_WORK}/Project/TypeRepository ${SAG_HOME}/common/DigitalEventServices/TypeRepository; fi

#RUN engine_deploy --outputDeployDir ${APAMA_WORK}/Project_deployed ${APAMA_WORK}/apama-mqtt-connect

RUN mkdir ${APAMA_WORK}/license
COPY --chown=sagadmin:sagadmin ApamaServerLicense.xml ${APAMA_WORK}/license/ApamaServerLicense.xml

#CMD ["correlator"]
ENTRYPOINT ["Project_deployed/start.sh"]
