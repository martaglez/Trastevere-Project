@echo off
docker-compose up -d
start /b python backend/appy.py
timeout /t 5
start http://localhost:5000
