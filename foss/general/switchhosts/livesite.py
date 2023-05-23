relnote = """livesite and testsite

livesite switches the test website back to the live site.

livesite checks the hosts file for the existence of entries for the test
website. If they exist the file gets re-written without them.

testsite switches the live website back to the test site.

testsite checks the hosts file for the existence of entries for the test
website. If they exist nothing happens. If not, test site entries are added.

Additionally (Windows only) testsite will execute (if it exists) a batch file
called 'proxy_remove.bat'. This exists in the same directory under a different
name 'proxy_remove_example.bat' as a precaution against unexpected execution.
See also two registry patch files in the same directory, similarly mis-named.
To make these work as expected edit both the content and names as desired.

When the test website goes live, it becomes the live site and livesite
should be run again finally so that the hosts file is no longer used to
find the website. By itself this proves that the DNS has been updated.

The source versions of livesite and testsite trigger an anti-virus warning
because they edit a system file. Just dismiss the warnings - provided they
occur exactly when you run one of these programs.

Version   Build Who When/What

rev 0.3.1 2722  md  14 Nov 2011 - rewrite xping.bat and rejig for line.example
rev 0.3.0 2705  md  27 Oct 2011 - reworked for addresses in ./lines.whatever
                                  and Popen to keep the batch pause on-screen
rev 0.2.1 2657  md  21 Oct 2010 - ensured file ends with \n
rev 0.2.0 2656  md  21 Oct 2010 - added registry edit to disable proxy
rev 0.1.0 2653  md  18 Oct 2010 - First written.

"""
__doc__ = relnote

import os, sys

win = False
if sys.platform.startswith('win'):
    win = True

if win:
    hostfile = os.path.join(os.environ['WINDIR'],
                            'system32\\drivers\\etc\\hosts')
    xping = 'xping.bat'
else:
    hostfile = '/etc/hosts'
    xping = 'ping'


linesdir = '.'

def getlines(fname='lines', linesdir=linesdir):
    # fetch the contents of fname.whatever
    lines = []
    for item in os.listdir(linesdir):
        if os.path.isfile(item) and item.startswith(fname):
            with open(item, 'r') as f:
                for line in f:
                    line = line.strip()
                    if len(line) > 7:
                        lines.append(line)
    return lines

lines = getlines()
if len(lines) < 1:
    print('No input file found')
    exit()

asite = '%s\n' % lines[0]
zsite = '%s\n' % lines[-1]

fsock = open(hostfile, 'r')
hostlines = fsock.readlines()
fsock.close()

if not hostlines[-1].endswith('\n'):
    hostlines[-1] = '%s\n' % hostlines[-1]


if asite in hostlines and zsite in hostlines:
    # delete hosts lines and let DNS do the work --> live site
    # comment this if-block out in testsite.py
    x = hostlines.index(asite)
    y = hostlines.index(zsite)
    del hostlines[x:y+1]
    fsock = open(hostfile, 'w')
    fsock.writelines(hostlines)
    fsock.close()
'''

if not (asite in hostlines and zsite in hostlines):
    # put lines in hosts and subvert the DNS --> test site
    # comment this if-block out in livesite.py
    for line in lines:
        hostlines.extend('%s\n' % line)
    fsock = open(hostfile, 'w')
    fsock.writelines(hostlines)
    fsock.close()

    if win:
        cmd = os.path.join(os.getcwd(), 'proxy_remove.bat')
        try:
            os.system(cmd)
        except Exception:
            pass
'''


# now ping and see
ip, domain = asite.split()

if win:
    with open(xping, 'r') as fsock:
        pinglines = fsock.readlines()
        i = -1
        for item in pinglines:
            i += 1
            if item.startswith('echo Ping statistics for'):
                item = 'echo Ping statistics for %s\n' % ip
                pinglines[i] = item

    with open(xping, 'w') as fsock:
        fsock.writelines(pinglines)

from subprocess import Popen
cmd = '%s %s' % (xping, domain)
Popen(cmd)

