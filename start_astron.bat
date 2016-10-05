@echo off
title POTCO-PS - Astron
cd astron

:main
astrond.exe --loglevel info config/cluster.yml
goto main
