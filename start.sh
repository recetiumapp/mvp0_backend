#!/usr/bin/env bash
export PYTHONPATH=/opt/render/project/src/src:$PYTHONPATH
gunicorn main:app --chdir src --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
