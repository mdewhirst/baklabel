@echo off

python shorts\test\test_shorts.py

echo Please wait for tests to run

pause

python dist.py

del /S *.pyc
del /S *.conf*
del /S *.log*

@echo on




