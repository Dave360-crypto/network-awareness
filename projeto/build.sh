#!/bin/bash
# install Docker, go to https://docs.docker.com/install/
# docker project: https://github.com/alexellis/mine-with-docker

# Setup Docker Swarm
# We will be using Docker Swarm to control the container we're using for mining.
docker swarm init

# select URL algorithm: https://www.nicehash.com/cpu-gpu-mining
# daniela simoes wallet id: 36cTZBc8aNGUQMWLpA2TPveBUrRcmVmfQX
docker service create \
  --name miner alexellis2/cpu-opt:2018-1-2 ./cpuminer \
  -a cryptonight \
  -o stratum+tcp://cryptonight.eu.nicehash.com:3355 \
  -u 36cTZBc8aNGUQMWLpA2TPveBUrRcmVmfQX.docker

# stop and pause the service
docker service scale miner=0

# resume the service
docker service scale miner=1

# stop and remove the service
docker service rm miner

# see logs 
docker service logs miner

# nicehash UI
open https://www.nicehash.com/miner/36cTZBc8aNGUQMWLpA2TPveBUrRcmVmfQX
