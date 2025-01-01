#!/bin/bash

# Run seeder.py and wait for it to finish
python3 seeder.py

# Run FastAPI application
fastapi run main.py