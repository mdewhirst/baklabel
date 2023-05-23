longdesc = """jgbim establishes a directory structure according to jgbim.conf"""

longerdesc = """1. Create C:\climate\jgbim\conf\jgbim.conf

2. Edit jgbim.conf similar to the following:
- - - - - - - - - - - - - - - - - - - -
machine1 = H:\\backup\machine1
machine2 = H:\\backup\machine2
machine3 = H:\\backup\machine3

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

"""

source = """Source: http://svn.pczen.com.au/repos/pysrc/gpl3/jgbim/distrib/

"""

licence = """License
=======
This program is free software: you can redistribute it and/or modify it.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.

Mike Dewhirst
August 2012
miked@climate.com.au

"""

relnote = """jgbim - see below for description
=======

Version    Build   Who  When/What
=================================

ver 0.1.1  2734     md  29 aug 2012 - Open and close logfile to let it update
                    as the program runs

ver 0.1.0  2733     md  28 aug 2012 - Added verbosity and loglevel

ver 0.0.0  2726     md  21 aug 2012 - first written


Description
===========
%s

%s

%s

%s
""" % (longdesc, longerdesc, source, licence)

__doc__ = relnote

import os, time, datetime

progname = 'jgbim'

class Writer(object):
    """Writes the directories listed in the ini file."""

    def __init__(self,
                 conf='C:\\climate\\%s\\conf\\%s.conf' % (progname, progname),
                 verbosity=1,
                 loglevel=3):
        self.abandon = False
        self.conf = conf
        self.verbosity = verbosity
        self.loglevel = loglevel
        self.confdir = os.path.split(conf)[0]
        self.logdir =  os.path.join(os.path.split(self.confdir)[0], 'log')
        self.log = os.path.join(self.logdir, '%s.log' % progname)
        self.pollinterval = 5 * 60
        self.servers = list()
        self.backupdirs = list()
        if not os.path.isdir(self.confdir):
            os.mkdir(self.confdir)
        if not os.path.isdir(self.logdir):
            os.mkdir(self.logdir)
        try:
            self.fconf = open(self.conf, 'r')
            self.getnoiselevel()
            self.getbackupdirs()
            self.getpollinterval()
            x = self.pollinterval / 60.0
            self.logthis('poll interval = %s mins' % x, level=1)
            self.logthis('verbosity = %s' % self.verbosity, level=1)
            self.logthis('loglevel = %s' % self.loglevel, level=1)
        except IOError:
            self.logthis('\nConfig file %s not found\n' % self.conf, level=-1)
            self.logthis(longerdesc, level=-1)
            self.abandon = True
        self.running = self.startup()


    def establishdir(self, server):
        if server:
            backupdir = 'not specified'
            try:
                idx = self.servers.index(server)
                backupdir = self.backupdirs[idx]
                drive, pth = os.path.splitdrive(backupdir)
                drive += '\\'
                if os.path.isdir(drive):
                    if not os.path.isdir(backupdir):
                        try:
                            os.makedirs(backupdir)
                        except OSError as e:
                            self.logthis('%s' % e, -1)
                    else:
                        self.logthis('directory %s already exists' % backupdir, level=2)
                else:
                    self.logthis('drive %s not available' % drive, level=2)
            except KeyError:
                self.logthis('server %s backup dir %s' % (server, backupdir), level=-1)


    def getnoiselevel(self):
        self.fconf.seek(0)
        lines = self.fconf.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if "verbosity" in line and '=' in line:
                    bits = line.split('=')
                    try:
                        v = int(bits[1].strip())
                        self.verbosity = v
                    except TypeError:
                        self.logthis('error in %s\n ... %s' % (self.conf, line),
                                                                      level=-1)
                if 'loglevel' in line and '=' in line:
                    bits = line.split('=')
                    try:
                        g = int(bits[1].strip())
                        self.loglevel = g
                    except TypeError:
                        self.logthis('error in %s\n ... %s' % (self.conf, line),
                                                                      level=-1)

    def getbackupdirs(self):
        self.fconf.seek(0)
        lines = self.fconf.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '\\' in line and '=' in line:
                    bits = line.split('=')
                    assert('\\' in bits[1])
                    self.servers.append(bits[0].strip())
                    self.backupdirs.append(bits[1].strip())
                    self.logthis('server %s requires %s' % (bits[0], bits[1]), 1)


    def getpollinterval(self):
        self.fconf.seek(0)
        lines = self.fconf.readlines()
        for line in lines:
            if 'polling' in line and '=' in line:
                print(line)
                factor = 1
                bits = line.split('=')
                try:
                    x = int(bits[1].strip().split()[0])
                    if 'min' in line: factor = 60
                    if 'hr' in line: factor = 60 * 60
                    if 'hour' in line: factor = 60 * 60
                    self.pollinterval = x * factor
                except Exception as e:
                    self.logthis('%s' % e, level=-1)


    def logthis(self, line, level=0):
        if self.verbosity > 0:
            print(line)
        if level <= self.loglevel:
            with open(self.log, 'a') as self.flog:
                self.flog.write(line.strip()+'\n')


    def oktorun(self):
        return os.path.isfile(self.running)


    def startup(self):
        flagfile = os.path.join(self.confdir, 'delete_to_stop_%s.txt' % progname)
        if not self.abandon:
            if not os.path.isfile(flagfile):
                with open(flagfile, 'w') as f:
                    f.write('This file is created at startup and checked every %s secs\n' % self.pollinterval)
                    f.write('\nIf should be deleted to stop the program.\n')
            return flagfile



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':

    def get_now():
        return datetime.datetime.now().timetuple()

    writer = Writer()
    if not writer.abandon:
        n = get_now()
        writer.logthis('Started on %s-%s-%s at %s:%s:%s' % (n[2],n[1],n[0],
                                                            n[3],n[4],n[5]), 1)
        while True:
            if writer.oktorun():
                time.sleep(writer.pollinterval)
                for server in writer.servers:
                    writer.establishdir(server)
            else:
                n = get_now()
                writer.logthis('Stopped on %s-%s-%s at %s:%s:%s' % (n[2],n[1],n[0],
                                                                    n[3],n[4],n[5]), 1)
                break
    writer.flog.close()
