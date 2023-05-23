@echo off

xcopy ..\baklabel\baklabel\*.py filemov /s /y /i

echo Please wait for baklabel tests to run

python filemov\test\test_baklabel.py

echo Please wait for filemov tests to run

python filemov\test\test_filemov.py

pause

python dist.py

del filemov\baklabel.py
del filemov\test\test_baklabel.py
del /S *.pyc
del /S *.conf*
del /S *.log*

@echo on




