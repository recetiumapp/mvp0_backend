# Paso 1: Establece el PYTHONPATH
export PYTHONPATH=./src:$PYTHONPATH 

# Paso 2: Ejecuta Uvicorn apuntando al módulo (la forma correcta)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload