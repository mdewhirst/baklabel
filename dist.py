#! /usr/bin/python

"""
1. read source to get the version number
2. update setup.py with the ver number
3. get release notes from baklabel docstring and put them into distrib too
4. call dist.bat to run tests and py2exe
5. create a self-extractor and put it in distrib

"""
#1
import os, sys
import shutil

sys.path.append(os.path.realpath(os.path.dirname(__file__)).replace('\\', '/'))

# Remove the build folder from the cwd
shutil.rmtree("build", ignore_errors=True)
# do the same for dist folder
shutil.rmtree("dist", ignore_errors=True)

version = '0.0.0'
build = '1234'
pyver = '-py%s' % sys.version[0:3]

with open('./pyver.txt', 'w') as fsock:
    fsock.write(pyver)

source = os.path.join(os.curdir, 'baklabel', 'baklabel.py')
fsock = open(source, 'r')
for line in fsock.readlines():
    if line.startswith('ver'):
        bits = line.split()
        version = bits[1].strip()
        build = bits[2].strip()
        break
fsock.close()

version = '%s-%s' % (version, build)

#2 update setup.py with the version and build numbers
setupsource = os.path.join(os.curdir, 'setup.py')
fsock = open(setupsource, 'r')
lines = fsock.readlines()
fsock.close()

i = -1
for line in lines:
    i += 1
    if line.startswith('version'):
        bits = line.split('=')
        # put in ver-build
        lines[i] = "%s='%s'\n" % (bits[0], version)
        break

fsock = open(setupsource, 'w')
fsock.writelines(lines)
fsock.close()

#3

from baklabel import baklabel

relnote = os.path.join('baklabel', 'doc', 'release_note.txt')
fsock = open(relnote, 'w')
fsock.writelines(baklabel.__doc__)
fsock.close()

about = os.path.join('baklabel', 'doc', 'about.txt')
fsock = open(about, 'w')
fsock.write('baklabel.py %s\n\n' % version)
fsock.writelines(baklabel.source)
fsock.close()

synopsis = os.path.join('baklabel', 'doc', 'synopsis.txt')
fsock = open(synopsis, 'w')
fsock.writelines(baklabel.Grandad.synopsis)
fsock.close()

readme = 'README.txt'
fsock = open(readme, 'w')
fsock.writelines(baklabel.longdesc)
fsock.writelines(baklabel.longerdesc)
fsock.writelines(baklabel.source)
fsock.close()

