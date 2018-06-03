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
  # coinbase wallet id

# other algorithms

#Scrypt
#stratum+tcp://scrypt.LOCATION.nicehash.com:3333
docker service create \
  --name miner alexellis2/cpu-opt:2018-1-2 ./cpuminer \
  -a scrypt \
  -o stratum+tcp://scrypt.eu.nicehash.com:3333 \
  -u 36cTZBc8aNGUQMWLpA2TPveBUrRcmVmfQX.docker

#x11
#stratum+tcp://x11.LOCATION.nicehash.com:3336
docker service create \
  --name miner alexellis2/cpu-opt:2018-1-2 ./cpuminer \
  -a x11 \
  -o stratum+tcp://x11.eu.nicehash.com:3336 \
  -u 36cTZBc8aNGUQMWLpA2TPveBUrRcmVmfQX.docker

# Keccak
#stratum+tcp://keccak.LOCATION.nicehash.com:3336
docker service create \
  --name miner alexellis2/cpu-opt:2018-1-2 ./cpuminer \
  -a keccak \
  -o stratum+tcp://keccak.eu.nicehash.com:3338 \
  -u 36cTZBc8aNGUQMWLpA2TPveBUrRcmVmfQX.docker

#NeoScrypt
#stratum+tcp://neoscrypt.LOCATION.nicehash.com:3336
docker service create \
  --name miner alexellis2/cpu-opt:2018-1-2 ./cpuminer \
  -a neoscrypt \
  -o stratum+tcp://neoscrypt.eu.nicehash.com:3341 \
  -u 36cTZBc8aNGUQMWLpA2TPveBUrRcmVmfQX.docker

#Quark
docker service create \
  --name miner alexellis2/cpu-opt:2018-1-2 ./cpuminer \
  -a quark \
  -o stratum+tcp://quark.eu.nicehash.com:3345 \
  -u 36cTZBc8aNGUQMWLpA2TPveBUrRcmVmfQX.docker

#Lyra2REv2
docker service create \
  --name miner alexellis2/cpu-opt:2018-1-2 ./cpuminer \
  -a lyra2rev2 \
  -o stratum+tcp://lyra2rev2.eu.nicehash.com:3347 \
  -u 36cTZBc8aNGUQMWLpA2TPveBUrRcmVmfQX.docker

# Blake256r8
docker service create \
  --name miner alexellis2/cpu-opt:2018-1-2 ./cpuminer \
  -a blake256r8 \
  -o stratum+tcp://blake256r8.eu.nicehash.com:3349 \
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
