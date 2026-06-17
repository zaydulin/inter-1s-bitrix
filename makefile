THIS_FILE := $(lastword $(MAKEFILE_LIST))
COMPOSE_FILE := docker-compose.yml
APP_SERVICE := moedelolk
.PHONY: help build run stop restart  destroy log shell manage makemigrations migrate test

help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null |	awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

build:
	docker-compose -f $(COMPOSE_FILE) build $(c)
run:
	docker-compose -f $(COMPOSE_FILE) up -d $(c)
stop:
	docker-compose -f $(COMPOSE_FILE) stop $(c)
restart:
	docker-compose -f $(COMPOSE_FILE) stop $(c)
	docker-compose -f $(COMPOSE_FILE) up -d $(c)
destroy:
	docker-compose -f $(COMPOSE_FILE) down -v $(c)
log:
	docker-compose -f $(COMPOSE_FILE) logs --tail=150 -f $(APP_SERVICE)
shell:
	docker-compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) /bin/bash
manage:
	docker-compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) python manage.py $(c)
makemigrations:
	docker-compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) python manage.py makemigrations
migrate:
	docker-compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) python manage.py migrate
test:
	docker-compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) python manage.py test
