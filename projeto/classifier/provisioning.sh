#!/usr/bin/env bash
echo "--------------------"
echo "Run Rabbit MQ..."
echo "--------------------"

docker run \
    --detach \
    --name local-rabbit \
    --publish 5672:5672 \
    --publish 15672:15672 \
    rabbitmq:3.7.4-management