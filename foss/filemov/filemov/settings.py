#! /usr/bin/python

import os, time

"""Make a settings object which delivers all necessary params for filemov"""

SFILE = 'settings.conf'
CONFIG = os.path.join(os.getcwd(), SFILE)

def defaultsettingsconf(settingsfile=CONFIG):
    config = """#THIS FILE WAS CREATED AS: %s
#
# config settings for filemov.exe. Use the # sign at the beginning of a
# line to 'comment out' unwanted items

# This is the target folder within which to commence looking ...
STARTIN = |users|miked|py|gpl3|test_files

# The default is to consider all files subject of course to any
# exclusions listed below. Here you can use an asterisk wildcard plus
# any portion of a filename to restrict operations to just filenames
# containing that pattern. eg., *.pdf will only work on .pdf files.
# Currently this does not accept a list of patterns.
PATTERN = *

# Now for the destination for the files which qualify for removal.
#
# The special destinations 'year' and 'sub-year' are symbolic and operate
# in much the same way. The actual difference is noted below. They mean
# we plan to create a sub-folder named for the year of the file to be
# moved - then move or copy it in there. For example, a file with a
# modified (or accessed or created) date of 6-6-2004 will end up in a
# folder called something|2004
#
# Note: 'year' means ONLY look for old files in the STARTIN folder
# nominated and NOT in any sub-folders of STARTIN.
#
# Note: 'sub-year' means to look for old files in STARTIN sub-folders.
# Actual files in STARTIN will be ignored as will sub-folders of those
# sub-folders. Only the first-level of STARTIN sub-folders will be
# checked for candidate files.
#
# On the other hand if we are moving or copying whole trees of old files
# we need to name a real destination in which to plant the tree of files
# which match the file age/cutoff specification below.
#
# ...|<baklabel> means to generate an extra sub-directory to sit between
# the DESTINATION directory root and the tree of files being moved or
# copied. baklabel is the name of a program which provides a grandfather
# backup label which will be used for the extra destination sub-directory.
# Find it at http://svn.pczen.com.au/repos/gpl3/baklabel/distrib
# Please note that DESTINATION must come before LOGNAME in this file if
# you want to use the DESTINATION directory for the filemov log
#DESTINATION = year
DESTINATION = sub-year
#DESTINATION = |users|miked|py|gpl3|test
#DESTINATION = |users|miked|py|gpl3|test|<baklabel>

# SHORTEN only applies when when you want a real destination rather than
# the symbolic 'year' or 'sub-year'.
#
# SHORTEN means to only append the actual STARTIN folder (and sub-folders)
# without its preceding path on to the end of the destination folder. For
# example if STARTIN = |users|miked|py|gpl3|test_files and there were lots
# of sub-directories under ...|test_files then SHORTEN would split the
# root off STARTIN and put files into DESTINATION|test_files
SHORTEN = False
#SHORTEN = True

# Cutoff age of files in days - means older files will be processed.
# To include all files use CUTOFF = 0. Otherwise ten years is 3650, five
# is 1825, three is 1095, two years is 730
CUTOFF = 5000

# Choose whether to detect file age from the time it was last accessed,
# modified or created. Uncomment one only.
#DETECT = accessed
#DETECT = created
DETECT = modified

# 99 times out of a hundred you want to move files to unclutter the
# original folders. Use 'report' to preview results.
#
# Note: copy will not overwrite an existing file
#ACTION = copy
#ACTION = copy-overwrite
#ACTION = move
#ACTION = move-remove-empty-folders
ACTION = report
#ACTION = report-make-folders

# When copying and moving files a backup is created if there is a
# destination file in existence. That file is renamed by adding a
# tilde ( ~ ) to the end of the filename. It keeps it around while
# the copy or move takes place. The tilde file probably needs to be
# cleaned up afterwards to avoid cluttering up destination folders.
# If you want to keep these safety files make CLEANUP False.
CLEANUP = True
#CLEANUP = False

# To omit specific files from the process just put their names or
# fragments of their names in the following list. Note that this will
# omit files which are spread throughout the directory tree if the
# fragment you specify here is detected in the filename. Separate the
# items with a space between each.
#
EXCLUDE_FILES = .htaccess thumbs.db .svn Desktop.ini

# Use EXCLUDE_DIRS if you wish to avoid ALL folders with the same
# name or fragment of a name spread throughout the directory tree.
# List those fragments here. Separate names with spaces.
#
EXCLUDE_DIRS = .svn

# If you have a whole branch of the directory tree you wish to
# omit from the process then use the SKIPFLAG method instead. In
# any folder create a file and rename it to whatever SKIPFLAG is
# set to here ...
SKIPFLAG = skipthis.dir

# You can choose to make this SKIPFLAG mechanism skip folders silently
# or have its exclusions noted in the log ...
SKIPSILENT = False

# The log (or report) is displayed after the process so you can save
# it for later perusal. You can choose a log name to suit yourself.
# DESTINATION as a symbolic location is usually a good idea. The actual
# destination can be anywhere you nominate and that is where the log
# (and the settings actually used) will end up - with today's date in the
# filename(s).
#
#LOGNAME = filemov.log
#LOGNAME = .|log|filemov.log
LOGNAME = DESTINATION|filemov.log

# The LOGNAME naming style you select above will be automatically
# changed to include the date like this: ..|2010_02_28_filemov.log

# If you are doing a lot of work on a single day you may wish to keep
# all the records in a single log file - in which case False is what
# you want here ...
#
#OVERWRITE_LOG = False
OVERWRITE_LOG = True

# Note that the actual settings used (this settings.conf file) will be
# written out alongside the log file wherever that ends up according
# to your LOGNAME setting above.
#
# Also note that these "factory defaults" can be retrieved by deleting
# (or renaming) this file from the filemov working directory. The
# next time filemov runs, this settings.conf will be recreated as new.

# Finally, you can adjust performance by yielding some CPU time back to
# the computer so it can work on other things at the same time. The
# higher the SNOOZE number the more time you give back but the slower
# filemov will run. SNOOZE = 0 is obviously fastest.  But SNOOZE = 0.1
# might be enough to keep other things on the computer ticking along.
#SNOOZE = 0
SNOOZE = 0.1
#SNOOZE = 1
#SNOOZE = 2
#SNOOZE = 4
#SNOOZE = 8
#SNOOZE = 16
#
""" % settingsfile
    return config.replace('|', os.path.sep)


# establish base zero defaults to be over-ridden by settings.conf
# TILDE must never be blank or backup file creation will fail
TILDE = '~'                 # not in settings.conf
YEAR = 'year'
SUBYEAR = 'sub-year'
ACCESSED = 'accessed'   # problematic on Windows/Novell
CREATED = 'created'     # problematic eg after restoring from backup
MODIFIED = 'modified'

STARTIN = os.path.join('foo', 'bar')
PATTERN = '*'
DESTINATION = '/bar/foo/'
SHORTEN = False
CUTOFF = 5000.0
DETECT = MODIFIED       # this is the default trigger
ACTION = 'report'       # safe default
CLEANUP = True
EXCLUDE_FILES = '.htaccess thumbs.db .svn Desktop.ini'
EXCLUDE_DIRS = '.svn'
SKIPFLAG = 'skipthis.dir'
SKIPSILENT = False
LOGNAME = os.path.join(os.getcwd(), 'filemov.log')
OVERWRITE_LOG = True
SNOOZE = 0


class Settings(object):
    """Contain all the defaults and override any/all with values found
    in a named settings file. For testing. we also need a mechanism for
    adjusting named settings directly"""

    def __init__(self, settingsfile=CONFIG,
        # following args are only used by test_filemov although in future
        # we might provide some cmdline args which would use these too.
                    startin=None,
                     pattern=None,
                      destination=None,
                       shorten=None,
                        cutoff=None,
                         detect=None,
                          action=None,
                           cleanup=None,
                            exclude_files=None,
                             exclude_dirs=None,
                              skipflag=None,
                               skipsilent=None,
                                logname=None,
                                 overwrite_log=None,
                                  snooze=None,
        ):
        # establish internal constants
        self.TILDE = TILDE
        self.YEAR = YEAR
        self.SUBYEAR = SUBYEAR
        self.ACCESSED = ACCESSED
        self.CREATED = CREATED
        self.MODIFIED = MODIFIED
        # establish base zero defaults
        self.STARTIN = STARTIN
        self.PATTERN = PATTERN
        self.DESTINATION = DESTINATION
        self.SHORTEN = SHORTEN
        self.CUTOFF = CUTOFF
        self.DETECT = DETECT
        self.ACTION = ACTION
        self.CLEANUP = CLEANUP
        self.EXCLUDE_FILES = EXCLUDE_FILES
        self.EXCLUDE_DIRS = EXCLUDE_DIRS
        self.SKIPFLAG = SKIPFLAG
        self.SKIPSILENT = SKIPSILENT
        self.LOGNAME = LOGNAME
        self.OVERWRITE_LOG = OVERWRITE_LOG
        self.SNOOZE = SNOOZE

        # next obtain/create the nominated settingsfile
        if not os.path.isfile(settingsfile):
            # create from scratch in the nominated location
            try:
                # we first need a directory
                os.makedirs(os.path.split(settingsfile)[0])
            except OSError:
                # delivers an OSError if the dir exists
                pass

            try:
                # and now the non-existent settingsfile
                with open(settingsfile, 'w') as fsock:
                    fsock.write(defaultsettingsconf(settingsfile).replace('''
''', os.linesep))
            except Exception as e:
                print('Failed to write settings to %s\n%s' % (settingsfile, e))

        self.CONFIG = settingsfile
        #self.CONF = os.path.split(settingsfile)[1]

        # the nominated settingsfile now exists - if it didn't previously

        def linebad(line):
            line = line.strip()
            if len(line) == 0: return True, []
            elif line[0] == '#': return True, []
            elif line[0] == '"': return True, []
            # ? is upper case sensitivity necessary ?
            # elif line[0] != line[0].upper(): return True, []
            bits = line.split("=", 1)
            if len(bits) == 2:
                bits[0] = bits[0].strip().upper()
                bits[1] = bits[1].strip()
            else:
                return True, [] # True - it is bad!
            return False, bits # meaning not bad and here's the var pair

        # now get the user edited settings to replace the defaults
        try:
            with open(self.CONFIG, 'r') as conf:
                for line in conf:
                    bad, pair = linebad(line)
                    if bad: continue
                    if pair[0] == 'STARTIN': self.STARTIN = pair[1]
                    elif pair[0] == 'PATTERN': self.PATTERN = pair[1]
                    elif pair[0] == 'SKIPFLAG': self.SKIPFLAG = pair[1]
                    elif pair[0] == 'SKIPSILENT':
                        if pair[1].lower() == 'true': self.SKIPSILENT = True
                        else: self.SKIPSILENT = False
                    elif pair[0] == 'DESTINATION':
                        self.DESTINATION = pair[1]
                    elif pair[0] == 'SHORTEN':
                        if pair[1].lower() == 'true': self.SHORTEN = True
                        else: self.SHORTEN = False
                    elif pair[0] == 'CUTOFF': self.CUTOFF = float(pair[1])
                    elif pair[0] == 'DETECT': self.DETECT = pair[1]
                    elif pair[0] == 'ACTION': self.ACTION = pair[1]
                    elif pair[0] == 'CLEANUP':
                        if pair[1].lower() == 'true': self.CLEANUP = True
                        else: self.CLEANUP = False
                    elif pair[0] == 'EXCLUDE_DIRS': self.EXCLUDE_DIRS = pair[1]
                    elif pair[0] == 'EXCLUDE_FILES': self.EXCLUDE_FILES = pair[1]
                    elif pair[0] == 'LOGNAME':
                        self.LOGNAME = pair[1]
                    elif pair[0] == 'OVERWRITE_LOG':
                        if pair[1].lower() == 'true': self.OVERWRITE_LOG = True
                        else: self.OVERWRITE_LOG = False
                    elif pair[0] == 'SNOOZE':
                        self.SNOOZE = self.getsleep(pair[1])
        except Exception:
            raise

        """ we have three text files: settingsfile, logname and settingsused

        logname and settingsused always go together and always gain a date.

        settingsfile (self.CONFIG) is nominated or defaults to os.getcwd()
        this is totally independent of where the other two end up.

        logname (self.LOGNAME) defaults to getcwd if it is just a filename.
        If it has any path, then it goes there as yyyy-mm-dd_<filemovlog>.

        Therefore we need to play with these after logname is finalised in
        the passed-in args
        """
        # now we need to override settings from any passed in *args

        def ifnone(arg1, arg2):
            # this leaves settings.conf values if args have not been offered
            if arg1 is None: return arg2
            else: return arg1

        self.STARTIN = ifnone(startin, self.STARTIN)
        self.PATTERN = ifnone(pattern, self.PATTERN)
        self.SHORTEN = bool(ifnone(shorten, self.SHORTEN))
        self.CUTOFF = float(ifnone(cutoff, self.CUTOFF))
        self.DETECT = ifnone(detect, self.DETECT)
        self.DESTINATION = ifnone(destination, self.DESTINATION)
        self.ACTION = ifnone(action, self.ACTION)
        self.CLEANUP = bool(ifnone(cleanup, self.CLEANUP))
        self.LOGNAME = ifnone(logname, self.LOGNAME)
        self.EXCLUDE_FILES = ifnone(exclude_files, self.EXCLUDE_FILES)
        self.EXCLUDE_DIRS = ifnone(exclude_dirs, self.EXCLUDE_DIRS)
        self.SKIPSILENT = bool(ifnone(skipsilent, self.SKIPSILENT))
        self.LOGNAME = ifnone(logname, self.LOGNAME)
        self.OVERWRITE_LOG = bool(ifnone(overwrite_log, self.OVERWRITE_LOG))
        self.SNOOZE = self.getsleep(ifnone(snooze, self.SNOOZE))

        dd = time.localtime()
        ddate = '%02d-%02d-%02d' % (dd.tm_year, dd.tm_mon, dd.tm_mday)

        # check to make sure logname has a path component
        if self.LOGNAME is None:
            self.logname = LOGNAME  # includes cwd
        else:
            bits = self.LOGNAME.split(os.path.sep)
            if len(bits) == 1:  # no path so put into getcwd()
                self.LOGNAME = os.path.join(os.getcwd(), self.LOGNAME)

        # at this point self.LOGNAME has a path component
        # but it may change if destination is a year or sub-year
        pth, log = self.checkdestinationlogname()
        # and then pth could be adjusted if startin doesn't exist
        pth = self.makelogpath(pth, log)
        # pth is now final
        self.LOGNAME = os.path.join(pth, '%s_%s' % (ddate, log))
        # use pth for settingsused no matter where settingsfile is
        parts = os.path.split(settingsfile)
        #
        self.SETTINGS_USED = os.path.join(pth, '%s_%s' % (ddate, parts[1]))

        # end of __init__()

    def checkdestinationlogname(self):
        """if DESTINATION has been detected in the pair[1] logname adjust the
        path component to put the log into the root of the destination dir"""
        pth, log = os.path.split(self.LOGNAME)
        if self.LOGNAME.find('DESTINATION') > -1:
            # pth would be startin if dest is year or sub-year
            if self.DESTINATION.find(YEAR) > -1:
                pth = self.STARTIN
            elif self.DESTINATION.find('<') > -1:
                pth = self.dest_baklabel()
            else:
                pth = self.DESTINATION
        if len(pth) == 0:
            pth = os.getcwd()
        return pth, log

    def makelogpath(self, pth, log):
        # check everything is OK because used settings are kept here too
        chkname = os.path.join(pth, log)
        if os.path.isfile(chkname):
            # obviously the pth exists
            if self.OVERWRITE_LOG:
                bak = chkname + TILDE
                if os.path.isfile(bak):
                    os.remove(bak)
                os.rename(chkname, bak)
            #else we can rely on appending to the log
        else:
            # better check that the directory exists!
            # we don't want to make a pth if startin ain't there
            # because that is a showstopper in filemov. However,
            # we do want a valid place for the log so we can show
            # the error to the user. We'll use the cwd
            if os.path.isdir(self.STARTIN):
                try:
                    os.makedirs(pth)
                except OSError:
                    pass # ok if it already exists
            else:
                pth = os.getcwd()
        return pth


    def dest_baklabel(self):
        destroot = self.DESTINATION
        desttail = ''
        x = self.DESTINATION.find('<')
        if x > -1:
            from baklabel import Grandad
            grandpa = Grandad(smallhours=6)
            destroot = self.DESTINATION[0:x] + grandpa.label()
            del(grandpa)
            y = self.DESTINATION.find('>')
            if y > x and y < len(self.DESTINATION):
                desttail = self.DESTINATION[y + 1:]
        return destroot + desttail

    def getsleep(self, seconds):
        try:
            zzzz = float(seconds)
            if zzzz < 0.00001:
                return float(0)
            else:
                return float(zzzz/100)
        except Exception:
            return float(SNOOZE)

    def printsettings(self, heading):
        print('\n%s' % heading)
        print('STARTIN = %s' % self.STARTIN)
        print('PATTERN = %s' % self.PATTERN)
        print('DESTINATION = %s' % self.DESTINATION)
        print('SHORTEN = %s' % self.SHORTEN)
        print('CUTOFF = %s' % self.CUTOFF)
        print('DETECT = %s' % self.DETECT)
        print('ACTION = %s' % self.ACTION)
        print('CLEANUP = %s' % self.CLEANUP)
        print('EXCLUDE_FILES = %s' % self.EXCLUDE_FILES)
        print('EXCLUDE_DIRS = %s' % self.EXCLUDE_DIRS)
        print('SKIPFLAG = %s' % self.SKIPFLAG)
        print('SKIPSILENT = %s' % self.SKIPSILENT)
        print('LOGNAME = %s' % self.LOGNAME)
        print('OVERWRITE_LOG = %s' % self.OVERWRITE_LOG)
        print('SNOOZE = %s' % self.SNOOZE)
        print('SETTINGS_USED = %s' % self.SETTINGS_USED)

