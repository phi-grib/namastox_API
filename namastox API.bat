@echo off
@CALL "%userprofile%\miniconda3\condabin\activate" namastox
START /REALTIME "namastox server" python app.py
REM START /REALTIME "" "http://localhost:5000/namastox/v1/list"