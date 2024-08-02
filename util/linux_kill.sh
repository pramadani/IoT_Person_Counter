#!/bin/bash

sudo kill -9 $(sudo lsof -t -i:65432)
sudo kill -9 $(sudo lsof -t -i:8501)