@echo off
echo Please wait for tests to run

if %1xx == xx (
set bld=end
set upl=end
) else (
set bld=build
set upl=upload
)

set py=311

C:\Python%py%\python src\baklabel\test_baklabel.py

if %bld% == end goto end

echo Build distribution wheel

pause

C:\Python%py%\python dist.py

C:\Python%py%\python -m build

if %upl% == end goto end

echo Upload distribution

pause

twine upload dist/*
:end
@echo on




