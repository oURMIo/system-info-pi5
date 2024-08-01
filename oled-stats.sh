#!/bin/bash


PROJECT_NAME=/system-info-pi5
PATH_TO_PROJECT=/path


source $PATH_TO_PROJECT/$PROJECT_NAME/venv/bin/activate
python $PATH_TO_PROJECT/$PROJECT_NAME/oled_system_status.py
