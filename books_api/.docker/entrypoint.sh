#!/bin/bash
gunicorn --bind 0.0.0.0:8000 --workers 3 books_api.wsgi:application