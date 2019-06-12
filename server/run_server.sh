#!/usr/bin/env bash
export FLASK_APP=server.py
. venv/bin/activate
flask run --host=0.0.0.0
