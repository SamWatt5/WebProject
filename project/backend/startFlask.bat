@echo off
cd src
call .venv/scripts/activate
py -m flask run --host=0.0.0.0 --port=8000