#! /usr/bin/python

"""
1.  Clean out the old builds
2.  read the source and obtain version
3.  write out the release note and other bits from docstrings

4.  edit setup_sdist.py to carry new version info
5.  copy sdist to setup.py and run it
6.  copy necessary files to distrib

7.  edit setup_py2exe.py to carry new version info
8.  copy py2exe to setup.py and run it
9.  zip up results for distribution
10. copy necessary files to distrib


"""
import os, sys
import shutil

wrkdir = os.path.dirname(os.path.realpath(__file__))
olddir = os.path.join(os.path.split(wrkdir)[0], 'old')

print(wrkdir)
print(olddir)

#1. Clean out the old builds

def begone(fileordir):
    if os.path.isdir(fileordir):
        shutil.rmtree(fileordir, ignore_errors=True)
    else:
        try:
            os.remove(fileordir)
        except OSError as e:
            if 'Error 2' in e:
                pass

begone(os.path.join(wrkdir, 'build'))
begone(os.path.join(wrkdir, 'dist'))
begone(os.path.join(wrkdir, 'jgbim', 'doc', 'release_note.txt'))
begone(os.path.join(wrkdir, 'jgbim', 'doc', 'about.txt'))
begone(os.path.join(wrkdir, 'jgbim', 'doc', 'README.txt'))
begone(os.path.join(wrkdir, 'README.txt'))
begone(os.path.join(wrkdir, 'MANIFEST'))

#2. read the source and obtain version

version = '0.1.0'
build = '2733'
pyver = 'py%s' % sys.version.split()[0][:3]
source = os.path.join(wrkdir, 'jgbim', 'jgbim.py')
fsock = open(source, 'r')
for line in fsock.readlines():
    if line.startswith('ver '):
        bits = line.split()
        version = bits[1].strip()
        build = bits[2].strip()
        break
fsock.close()

revision = version
version = '%s-%s-%s' % (version, build, pyver)

print(version)

#3. write out the release note and other bits from docstrings

from jgbim import jgbim

relnote = os.path.join(wrkdir, 'jgbim', 'doc', 'release_note.txt')
with open(relnote, 'w') as f:
    f.writelines(jgbim.__doc__)

about = os.path.join(wrkdir, 'jgbim', 'doc', 'about.txt')
with open(about, 'w') as f:
    f.write('jgbim.py %s\n\n' % version)
    f.writelines(jgbim.source)

licence = os.path.join(wrkdir, 'jgbim', 'doc', 'license.txt')
with open(licence, 'w') as f:
    f.write('jgbim.py \n\n')
    f.writelines(jgbim.licence)

readme = os.path.join(wrkdir, 'README.txt')
with open(readme, 'w') as f:
    f.write('jgbim - a Python program\n')
    f.write('\n')
    f.writelines(jgbim.longdesc)
    f.write('\n')
    f.write('\n')
    f.write('Howto\n')
    f.write('\n')
    f.writelines(jgbim.longerdesc)
    f.write('\n')
    f.write('\n')
    f.writelines(jgbim.source)


if 'py2' in pyver:
    # py2exe
    #7. edit setup_py2exe.py to carry new version info

    lines = list()
    py2exesource = os.path.join(wrkdir, 'setup.py')
    with open(py2exesource, 'r') as f:
        lines = f.readlines()

    i = -1
    for line in lines:
        i += 1
        sline = line.strip()
        if sline.startswith('ver'):
            lines[i] = "version = '%s'\n" % revision
        if sline.startswith('python'):
            lines[i] = "python = 'Python %s'\n" % pyver[2:]
            break

    with open(py2exesource, 'w') as f:
        f.writelines(lines)


    #8. copy py2exe to setup.py and run it


    src = os.path.join(wrkdir, 'README.txt')
    dst = os.path.join(wrkdir, 'jgbim', 'doc', 'README.txt')
    if os.path.isfile(src):
        shutil.copy(src, dst)

    os.system('python setup.py py2exe')

    #9 - zip up results for distribution

    os.chdir(os.path.join(wrkdir, 'dist'))

    zipfile = 'jgbim-%s-%s-%s-win32-setup' % (revision, build, pyver)

    optz = [
    r'C:\PROGRA~1\WinZip\WZZIP.EXE',
    r'-ex',
    r'-p',
    r'-r',
    zipfile + '.zip',
    r'*.*'
    ]
    os.system(' '.join(optz))

    opts = [
    r'C:\PROGRA~1\WinZip\WZIPSE32.EXE',
    zipfile + '.zip',
    r'-y',
    r'-d C:\climate\jgbim',
    r'-m ..\jgbim\doc\jgbim_setup.message.txt',
    r'-le',
    r'-overwrite',
    r'-st"jgbim %s"' % version,
    r'-a ..\jgbim\doc\about.txt',
    #r'-c ..\README.txt'
    ]
    os.system(' '.join(opts))

    os.chdir(wrkdir)

    #10. copy necessary files to distrib

    exefile = zipfile + '.exe'

    distdir = os.path.join(wrkdir, 'dist')
    distribdir = os.path.join(wrkdir, 'distrib')


    src = os.path.join(distdir, exefile)
    dst = os.path.join(distribdir, exefile)
    begone(dst)
    os.rename(src, dst)

