@echo off
@CALL "%userprofile%\miniconda3\condabin\activate" namastox
START /REALTIME "namastox server" python app.py