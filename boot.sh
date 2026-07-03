#!/bin/bash


/home/opeyemi/.pyenv/versions/billr/bin/uvicorn config.asgi:application --reload --host 0.0.0.0 --port 8000
