FROM python:3.12.2

# required for jenkins which run in kubernetis for docker in docker
RUN apt update && apt install podman -y

RUN useradd -rm -d /home/xfsc -s /bin/bash -g root -G sudo -u 1001 xfsc
USER xfsc
WORKDIR /home/xfsc
RUN echo 'export PATH=~/.local/bin:${PATH}' > .bashrc

RUN mkdir eu.xfsc.bdd.core
COPY --chown=xfsc setup.cfg setup.py eu.xfsc.bdd.core/
COPY --chown=xfsc src eu.xfsc.bdd.core/src

RUN ls -lah
RUN pip install -U pip wheel
RUN pip install "./eu.xfsc.bdd.core"

# validate
RUN python -c 'import eu.xfsc.bdd.core'
