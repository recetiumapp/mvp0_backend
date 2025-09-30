#!/usr/bin/env bash

# El comando indica: gunicorn [archivo_principal]:[objeto_app] --configuraciones
gunicorn src/main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
