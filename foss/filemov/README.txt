filemov - a Python program

filemov copies or moves 'x days old' files into other dirs as per
configured strategy. It is easy to use without mistakes.

Howto

1. Run filemov the first time to produce a fully commented set of
configuration settings called settings.conf. These are reproduced
at any time by deleting settings.conf and re-running filemov.

2. Edit settings.conf to suit your requirements and run filemov.

3. Examine the report to prove filemov did what you expected.

Features

- unclutter named dir using year-labelled subdirs for old files
- unclutter first-level dirs only with year-subdirs for old files
- copy/move whole directory tree
- copy, move, report-only, report-only + make-dirs
- report includes total file size and time taken plus each action
- destination tree can be auto-date-labelled for grandfathering
- exclude files by pattern
- exclude directories by pattern
- exclude directories by (skipthis.dir) flag
- automatically displays report on completion
- automatically re-presents settings.conf in system editor

Source:  Userid is 'public' with no password.
http://svn.pczen.com.au/repos/pysrc/gpl3/filemov/distrib/

Mike Dewhirst
miked@dewhirst.com.au
