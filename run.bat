@echo off
echo Running server.py
start cmd /k python app/server.py
echo Running sensor.py
start cmd /k python app/sensor.py
echo Running ui.py
start cmd /k streamlit run app/ui.py
