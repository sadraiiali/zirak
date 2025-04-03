#!/bin/bash 
# export PYTHONDONTWRITEBYTECODE=1
# export PYTHONUNBUFFERED=1
# export WORKERS_PER_CORE=1

uv sync

uv run python main.py
