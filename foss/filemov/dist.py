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

# dist.bat deletes distrib/*.exe and *.zip

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
begone(os.path.join(wrkdir, 'filemov', 'doc', 'release_note.txt'))
begone(os.path.join(wrkdir, 'filemov', 'doc', 'about.txt'))
begone(os.path.join(wrkdir, 'filemov', 'doc', 'README.txt'))
begone(os.path.join(wrkdir, 'README.txt'))
begone(os.path.join(wrkdir, 'MANIFEST'))
begone(os.path.join(wrkdir, 'settings.py'))
begone(os.path.join(wrkdir, 'baklabel.py'))

#2. read the source and obtain version

version = '0.0.0'
build = '1234'
pyver = 'py%s' % sys.version.split()[0][:3]
source = os.path.join(wrkdir, 'filemov', 'filemov.py')
fsock = open(source, 'r')
for line in fsock.readlines():
    if line.startswith('ver'):
        bits = line.split()
        version = bits[1].strip()
        build = bits[2].strip()
        break
fsock.close()

revision = version
version = '%s-%s-%s' % (version, build, pyver)

#3. write out the release note and other bits from docstrings

from filemov import filemov

relnote = os.path.join(wrkdir, 'filemov', 'doc', 'release_note.txt')
fsock = open(relnote, 'w')
fsock.writelines(filemov.__doc__)
fsock.close()

#relnote = os.path.join(olddir, 'filemov', 'doc', 'release_note.txt')
#fsock = open(relnote, 'w')
#fsock.writelines(filemov.__doc__)
#fsock.close()

about = os.path.join(wrkdir, 'filemov', 'doc', 'about.txt')
fsock = open(about, 'w')
fsock.write('filemov.py %s\n\n' % version)
fsock.writelines(filemov.source)
fsock.close()

#about = os.path.join(olddir, 'filemov', 'doc', 'about.txt')
#fsock = open(about, 'w')
#fsock.write('filemov.py %s\n\n' % version)
#fsock.writelines(filemov.source)
#fsock.close()

readme = os.path.join(wrkdir, 'README.txt')
fsock = open(readme, 'w')
fsock.write('filemov - a Python program\n')
fsock.write('\n')
fsock.writelines(filemov.longdesc)
fsock.write('\n')
fsock.write('\n')
fsock.write('Howto\n')
fsock.write('\n')
fsock.writelines(filemov.longerdesc)
fsock.write('\n')
fsock.write('\n')
fsock.writelines(filemov.source)
fsock.close()

#readme = os.path.join(olddir, 'README.txt') #, 'filemov', 'doc', 'README.txt')
#fsock = open(readme, 'w')
#fsock.write('filemov - a Python program\n')
#fsock.write('\n')
#fsock.writelines(filemov.longdesc)
#fsock.write('\n')
#fsock.write('\n')
#fsock.write('Howto\n')
#fsock.write('\n')
#fsock.writelines(filemov.longerdesc)
#fsock.write('\n')
#fsock.write('\n')
#fsock.writelines(filemov.source)
#fsock.close()


# sdist
#4. edit setup_sdist.py to carry new version info

sdistsource = os.path.join(wrkdir, 'setup_sdist.py')
fsock = open(sdistsource, 'r')
lines = fsock.readlines()
fsock.close()

i = -1
for line in lines:
    i += 1
    sline = line.strip()
    if sline.startswith('version'):
        lines[i] = "        version = '%s',\n" % version
        break

fsock = open(sdistsource, 'w')
fsock.writelines(lines)
fsock.close()

#5. copy sdist to setup.py and run it

fsockin = open(sdistsource, 'r')
fsockout = open('setup.py', 'w')
fsockout.writelines(fsockin.readlines())
fsockout.close()
fsockin.close()

# this creates build and dist dirs
os.system('python setup.py sdist')
os.system('python setup.py bdist_wininst --user-access-control auto')

#6. copy necessary files to distrib

distdir = os.path.join(wrkdir, 'dist')
distribdir = os.path.join(wrkdir, 'distrib')

zipz = 'filemov-%s.zip' % version
zipx =  'filemov-%s.win32.exe' % version

src = os.path.join(distdir, zipz)
dst = os.path.join(distribdir, zipz)
begone(dst)
os.rename(src, dst)

src = os.path.join(distdir, zipx)
dst = os.path.join(distribdir, zipx)
begone(dst)
os.rename(src, dst)

if 'py2' in pyver:
    # py2exe
    #7. edit setup_py2exe.py to carry new version info

    py2exesource = os.path.join(wrkdir, 'setup_py2exe.py')
    fsock = open(py2exesource, 'r')
    lines = fsock.readlines()
    fsock.close()

    i = -1
    for line in lines:
        i += 1
        sline = line.strip()
        if sline.startswith('version'):
            lines[i] = "version = '%s'\n" % revision
        if sline.startswith('python'):
            lines[i] = "python = 'Python %s'\n" % pyver[2:]
            break

    fsock = open(py2exesource, 'w')
    fsock.writelines(lines)
    fsock.close()


    #8. copy py2exe to setup.py and run it

    # but this needs settings.py and baklabel.py in wrkdir first

    src = os.path.join(wrkdir, 'filemov', 'settings.py')
    if os.path.isfile(src):
        shutil.copy(src, wrkdir)

    src = os.path.join(wrkdir, 'filemov', 'baklabel.py')
    if os.path.isfile(src):
        shutil.copy(src, wrkdir)

    src = os.path.join(wrkdir, 'README.txt')
    dst = os.path.join(wrkdir, 'filemov', 'doc', 'README.txt')
    if os.path.isfile(src):
        shutil.copy(src, dst)

    fsockin = open(py2exesource, 'r')
    fsockout = open('setup.py', 'w')
    fsockout.writelines(fsockin.readlines())
    fsockout.close()
    fsockin.close()

    os.system('python setup.py py2exe')

    #9 - zip up results for distribution

    os.chdir(os.path.join(wrkdir, 'dist'))

    zipfile = 'filemov-%s-%s-%s-win32-setup' % (revision, build, pyver)

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
    r'-d C:\climate\filemov',
    r'-m ..\filemov\doc\filemov_setup.message.txt',
    r'-le',
    r'-overwrite',
    r'-st"filemov %s"' % version,
    r'-a ..\filemov\doc\about.txt',
    r'-c ..\README.txt'
    ]
    os.system(' '.join(opts))

    os.chdir(wrkdir)

    #10. copy necessary files to distrib

    exefile = zipfile + '.exe'

    src = os.path.join(distdir, exefile)
    dst = os.path.join(distribdir, exefile)
    begone(dst)
    os.rename(src, dst)

begone(os.path.join(wrkdir, 'settings.py'))
begone(os.path.join(wrkdir, 'baklabel.py'))


