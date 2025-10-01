#!/usr/bin/env bash
export PYTHONPATH=./src:$PYTHONPATH 

gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT