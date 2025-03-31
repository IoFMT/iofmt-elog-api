#!/bin/bash

docker-compose -f ./docker-compose.yml down --rmi local --remove-orphans --volumes
docker volume prune -f
