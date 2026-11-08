@echo off
set PYTHONUTF8=1
cd /d C:\projects\bemyaccess.org\crawler
venv\Scripts\python.exe crawl.py >> run_output.log 2>&1
