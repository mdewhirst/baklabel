#! /usr/bin/python

"""
1. read livesite.py (or testsite.py) to get the revision number
2. update setup.py with the rev number and thisdir (being livesite)
3. get release notes from filemov docstring and put them into distrib too
4. call dist.bat to run tests and py2exe for livesite
5. create a self-extractor and put it in distrib

"""

#1
revision = '0.0.0'
site = 'testsite'
fsock = open('%s.py' % site, 'r')
for line in fsock.readlines():
    if line.startswith('rev'):
        bits = line.split()
        revision = bits[1]
        build = bits[2]
        break
fsock.close()

#2
fsock = open('setup.py', 'r')
lines = fsock.readlines()
fsock.close()

i = -1
for line in lines:
    i += 1
    if line.startswith('revision'):
        bits = line.split('=')
        lines[i] = "%s = '%s'\n" % (bits[0].strip(), revision)
        break
i = -1
for line in lines:
    i += 1
    if line.startswith('thisdir'):
        bits = line.split('=')
        lines[i] = "%s = '%s'\n" % (bits[0].strip(), site)
        break

fsock = open('setup.py', 'w')
fsock.writelines(lines)
fsock.close()

revision = revision + '_' + build

#3

relnote = r'.\distrib\release_note.txt'
fsock = open(relnote, 'w')
import livesite
fsock.writelines(livesite.__doc__)
fsock.close()


#4 - run tests and py2exe
import os
import shutil

os.system('dist.bat %s' % revision)

try:
    fname = './dist/%s.exe' % site
    if os.path.isfile(fname):
        shutil.copy(fname, './add')
except Exception:
    pass

"""
This being livesite we need testsite.exe before zipping and vice versa
"""

if site == 'testsite':
    other = 'livesite.exe'
else:
    other = 'testsite.exe'

if os.path.isfile('./add/%s' % other) :

    #5 - zip up results for distribution
    wdir = os.path.dirname(__file__)
    os.chdir(os.path.join(wdir, 'dist'))

    zipfile = r'switch_%s_setup' % revision

    optz = [
    r'C:\PROGRA~1\WinZip\WZZIP.EXE',
    r'-ex',
    r'-p',
    r'-r',
    zipfile + '.zip',
    r'*.*'
    ]
    os.system(' '.join(optz))

    destin = 'Switch'

    opts = [
    r'C:\PROGRA~1\WinZip\WZIPSE32.EXE',
    zipfile + '.zip',
    r'-y',
    r'-d %s' % destin,
    r'-m ..\add\switch_setup.message.txt',
    r'-le',
    r'-overwrite',
    r'-st"switch %s"' % revision,
    r'-a about.txt',
    r'-c instructions.txt',
    ]
    os.system(' '.join(opts))

    distrib = r'..\distrib\%s.exe' % zipfile
    zipfile = zipfile + '.exe'
    try: os.remove(distrib)
    except OSError: pass
    try: os.rename(zipfile, distrib)
    except OSError: pass

