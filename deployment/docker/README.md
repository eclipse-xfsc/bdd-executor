# To Compile, Build and Execute into Dockerized setup follow the commands:

## Build

Build images prod ``eu-xfsc-bdd-core`` and dev ``eu-xfsc-bdd-core-dev`` images.

:NOTE: To delimit local and pulled image,
we change TRAIN_DOCKER_IMAGE_TAG=latest-local [.env](.env),
default will be ``latest```.

```bash
$ cd deployment/docker
$ export TRAIN_DOCKER_IMAGE_TAG=latest-local && docker-compose up --build 
$ docker-compose images
CONTAINER               REPOSITORY                                                          TAG                 IMAGE ID            SIZE
eu-xfsc-bdd-core        node-654e3bca7fbeeed18f81d7c7.ps-xaas.io/dev-ops/bdd-executor       latest-local       fd3195468659        1.22GB
eu-xfsc-bdd-core-dev    node-654e3bca7fbeeed18f81d7c7.ps-xaas.io/dev-ops/bdd-executor-dev   latest-local       bfe84927c2c4        1.4GB
```

## Pull

```bash
$ docker pull node-654e3bca7fbeeed18f81d7c7.ps-xaas.io/dev-ops/bdd-executor
$ docker images | grep "train/bdd.*latest "
node-654e3bca7fbeeed18f81d7c7.ps-xaas.io/dev-ops/bdd-executor    latest    fd3195468659    2 months ago    1.22GB
```