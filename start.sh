#!/usr/bin/env bash
export PYTHONPATH=./src:$PYTHONPATH
gunicorn main:app --chdir . --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
