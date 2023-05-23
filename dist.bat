@echo off
echo Please wait for tests to run

if %1xx == xx (
set reg=
set upl=
) else (
set reg=register
set upl=upload
)

echo %reg% %upl%

\Python27\python baklabel\test\test_baklabel.py

\Python34\python baklabel\test\test_baklabel.py

pause

del MANIFEST


del pyver.run

\Python27\python dist.py

\Python27\python setup.py sdist

xcopy dist\*.zip distrib /y

ren pyver.txt pyver.run

\Python27\python setup.py %reg% bdist_wininst --user-access-control auto %upl%

xcopy dist\*.exe distrib /y


del pyver.run

\Python34\python dist.py

\Python34\python setup.py sdist

xcopy dist\*.zip distrib /y

ren pyver.txt pyver.run

\Python34\python setup.py %reg% sdist bdist_wininst --user-access-control auto %upl%

xcopy dist\*.exe distrib /y

@echo on




