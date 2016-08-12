@echo off
title Pirates Remake - Client

set /P PPYTHON_PATH=<PPYTHON_PATH
set GAME_SERVER=127.0.0.1
set LOGIN_COOKIE=dev

echo ==============================
echo Starting Pirates Online Remake...
echo Panda Python Path: %PPYTHON_PATH%
echo Username: %LOGIN_COOKIE%
echo Gameserver (IP): %GAME_SERVER%
echo ==============================
 
%PPYTHON_PATH% -m pirates.piratesbase.PiratesStart
pause
