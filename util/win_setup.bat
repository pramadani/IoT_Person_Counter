@echo off

python -m venv venv

call ./venv/Scripts/Activate

pip install -r ./util/requirements.txt