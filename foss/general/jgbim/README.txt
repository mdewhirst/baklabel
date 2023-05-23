jgbim - a Python program

jgbim establishes a directory structure according to jgbim.conf

Howto

1. Create C:\climate\jgbim\conf\jgbim.conf

2. Edit jgbim.conf similar to the following:
- - - - - - - - - - - - - - - - - - - -
machine1 = H:\backup\machine1
machine2 = H:\backup\machine2
machine3 = H:\backup\machine3

polling = 5 min

# verbosity applies to console output 0 = off, 1 = on
verbosity = 1

# loglevel 0 = off, 1 = minimal logging, 2 = everything
loglevel = 2

- - - - - - - - - - - - - - - - - - - -

3. Set up jgbim.exe to be executed when the machine is restarted

4. Examine the log from time to time to see what is happening

Features

- automatically test for the presence of the directories in the conf file
- if the directories do not exist, create them



Source: http://svn.pczen.com.au/repos/pysrc/gpl3/jgbim/distrib/

