#! /usr/bin/python

"""
1. read baklabel code to get the version number
2. update pyproject.toml with the ver number
3. get release notes from baklabel docstring and put them into doc

"""
import os, sys
import shutil

sys.path.append(os.path.realpath(os.path.dirname(__file__)).replace('\\', '/'))

# Remove the build folder from the cwd
shutil.rmtree("build", ignore_errors=True)
# do the same for dist folder
shutil.rmtree("dist", ignore_errors=True)

version = '0.0.0'

code = os.path.join(os.curdir, 'src', 'baklabel', 'baklabel.py')
fsock = open(code, 'r')
for line in fsock.readlines():
    if line.startswith('ver'):
        bits = line.split()
        version = bits[1].strip()
        break
fsock.close()

setupsource = os.path.join(os.curdir, 'pyproject.toml')
fsock = open(setupsource, 'r')
lines = fsock.readlines()
fsock.close()

i = -1
for line in lines:
    i += 1
    if line.startswith('version'):
        bits = line.split('=')
        lines[i] = f"{bits[0].strip()} = '{version}'\n"
        break
# rewrite with version from code
fsock = open(setupsource, 'w')
fsock.writelines(lines)
fsock.close()

# Assemble some docs

from src.baklabel import baklabel

relnote = os.path.join('.', 'doc', 'release_note.txt')
fsock = open(relnote, 'w')
fsock.writelines(baklabel.__doc__)
fsock.close()

about = os.path.join('.', 'doc', 'about.txt')
fsock = open(about, 'w')
fsock.write(f'baklabel.py {version}\n\n')
fsock.writelines(baklabel.repo)
fsock.close()

synopsis = os.path.join('.', 'doc', 'synopsis.txt')
fsock = open(synopsis, 'w')
fsock.writelines(baklabel.Grandad.synopsis)
fsock.close()

readme = 'README.md'
fsock = open(readme, 'w')
fsock.writelines(baklabel.readme())
fsock.close()

