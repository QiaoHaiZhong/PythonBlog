#!/bin/bash
gunicorn -w 2 -b 0.0.0.0:5000 wsgi:pyshell
