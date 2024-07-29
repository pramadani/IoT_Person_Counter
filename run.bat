@echo off
echo Running server.py
start cmd /k python server.py
echo Running sensor.py
start cmd /k python sensor.py
echo Running ui.py
start cmd /k streamlit run ui.py
