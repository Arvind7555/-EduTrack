@echo off
title EduTrack - Student Attendance & Grade Management System
echo ======================================================================
echo           EduTrack: Student Attendance & Grade Management
echo ======================================================================
echo.
echo Checking database initialization...
if not exist "data\school.db" (
    echo Populating sample demo data...
    python seed_data.py
)
echo.
echo Launching EduTrack Application on http://127.0.0.1:5000 ...
start "" "http://127.0.0.1:5000"
python app.py
pause
