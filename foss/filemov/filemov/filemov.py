from __future__ import print_function

longdesc = """filemov copies or moves 'x days old' files into other dirs as per
configured strategy. It is easy to use without mistakes."""

longerdesc = """1. Run filemov the first time to produce a fully commented set of
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
- automatically re-presents settings.conf in system editor"""

source = """Source:  Userid is 'public' with no password.
http://svn.pczen.com.au/repos/pysrc/gpl3/filemov/distrib/

Mike Dewhirst
miked@dewhirst.com.au
"""

relnote = """filemov - see below for description
=======

Version   Build Who When/What
=============================
todo                - Add command line arg to use different settings.conf
                    which requires all args to be part of a settings object

This means program flow will be ...

1. parse the argv for a named settings.conf file
   - if no file is there use the default conf from cwd
   - save the settings used in cwd WITH A LOUD TOP LINE of saved pathname
2. create an object with all the settings from the named conf
3. pass the object into filemov
4. launch the log for review
5. launch the named settings.conf for editing


                    - GUI interface for settings adjustments
                    - use compression for optional zip/tar.gz output


ver 0.0.0       md  1 jan 2010 - first written

ver 0.0.1       md  2 jan 2010 - improved time formatting and Win paths

ver 0.1.0 2571  md  13 jan 2010 - moved STARTIN testing out of settings.py
                    to here, added action = report-make-folders option,
                    cleaned up the 'directory visited' reporting and
                    included self.printing so output can be switched off
                    during unit tests.

ver 0.2.0 2573  md  20 jan 2010 - Added 'SHORTEN' option for dest paths

ver 0.2.1 2581  md  25 jan 2010 - repaired makedirs bug in settings.py and
                    added ' + past' to every test case with a cutoff value
                    so that when running tests you only need to increment
                    the past value in one place at the top of the suite to
                    make date based tests work. Included release_note.txt.

ver 0.3.3 2589  md  26 jan 2010 - catch trapped exception and filename for
                    log and added comma formatted totalsize, filecount.
                    Trapped file stat size date and Windows name errors
                    Trapped no date ValueError exception. Added file-size
                    and file-date to log. Changed date format to Australian


ver 0.4.0 2592  md  28 jan 2010 - added error collection to be appended to
                    the normal log on completion. Reformatted times to have
                    leading zeros for single digits.

ver 0.5.0 2593  md  2 feb 2010 - give log file a date-computed filename
                    and permit DESTINATION as a log folder. Also write out
                    the settings used alongside the log using the computed
                    filename. If the log and settings files exist in the
                    destination they get backed up with a trailing tilde.
                    Added finish time to the run to keep track of 'sleep'
                    impact on cpu. Added SNOOZE user setting to control
                    impact of 'sleep'.

ver 0.5.1 2596  md  3 feb 2010 - insert the original settings.conf (ie the
                    factory defaults) into settings.py as the docstring and
                    only write it out if the settings.py file does not
                    exist. This permits updates without overwriting any
                    pre-existing settings. Adjusted logfile location to
                    current working dir if the startin dir is invalid.

ver 0.5.2 2600  md  13 feb 2010 - adjust embedded settings.conf to work
                    under Linux with forward slashes and also include as
                    docstring in settings.py.

ver 0.5.3 2607  md  3 mar 2010 - added skipthis.dir feature to permit
                    exclusion of directories by leaving a specially named
                    file lying around in the directory to be avoided

ver 0.5.4 2608  md  4 mar 2010 - added skipsilent feature to provide a
                    choice as to whether skipped directories are logged
                    or not

ver 0.5.5 2622  md  11 apr 2010 - establish the current time once-only in
                    __init__() rather than repeatedly in is_candidate()
                    Refactored lightly and improved inline comments

ver 0.6.0 2623  md  20 apr 2010 - permit a wildcard * asterisk to operate
                    only on particular file name patterns.

ver 0.6.1 2624  md  22 apr 2010 - added -q option to switch off screen I/O

ver 0.7.0 2625  md  26 apr 2010 - added new action move-remove-empty-folders

ver 0.7.1 2626  md  27 apr 2010 - repaired dest_suffix bug which was chopping
                    off the leading character if shortening a windows root dir.
                    See unit test #65

ver 0.7.2 2630  md  6 may 2010 - repaired silent behaviour on Windows 2003
                    terminal server when it should be noisy.

ver 0.7.3 2631  md  14 may 2010 - added the list of skipthis.dir exclusions
                    to the end of the log for ease of checking afterwards.

ver 0.8.0 2650  md  11 Oct 2010 - Feature to import a generated label from
                    baklabel .py to include a grandfather element to the
                    destination path for the filemov'd files. Also, from
                    __future__ import print_function

ver 0.9             3 Nov 2010 - Skipped. Jumping from 0.8.0 to 1.0.0.

ver 1.0.0 2670  md  3 Nov 2010 - Enhanced to do case sensitive file
                    exclusions in non-Windows environments. In production.

ver 1.1.0 2683  md  18-Jan-2011 - refactored to use a settings object
                    to have the ability to use named settings files.
                    Changed YIELD to SNOOZE to avoid syntax highlighting
                    from using the python 'yield' word

ver 1.1.1 2728  md  24 Aug 2012 - Code review and tweaks to test importing
                    to cater for in-house python path adjustments

ver 1.1.2 2738  md  29 Jul 2013 - Now counting errors caught.

ver 1.2.0 2748  md  31 Jul 2013 - If a detected error code indicates the
                    pathname is too long on Windows, use the 8.3 pattern
                    to shorten things somewhat before writing it out. It
                    still remains an error but at least we have moved the
                    file. We need to retain the information lost while
                    shortening so we create a new file named after the
                    shortened name but with an extension .oldname.txt

ver 1.2.1 2754  md  8 Apr 2018 - Adjusted logging to permit switching it off
                    during testing. Python 3.6 warns about unclosed files so
                    rather than try harder and close log files it is easier
                    to avoid logging during tests.


Description
===========
%s

%s

%s

License
=======
Copyright (C) 2010 Mike Dewhirst

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" % (longdesc, longerdesc, source)

__doc__ = relnote

import os, shutil, time

try:
    import win32api
except ImportError:
    pass

import settings

# set up some ordinary constants ...
# is this Windows platform - ie., case-insensitive
WIN = (os.name == 'nt')
# a better word than True in is_excluded_dir() and is_exluded_file()
EXCLUDED = True
INCLUDED = not EXCLUDED

errorheader = '%s- - - - Errors below are also embedded in the log - - - -%s' % (os.linesep, os.linesep)
errorfooter = '%s- - - - See also errors above embedded in the log - - - -%s' % (os.linesep, os.linesep)

class Stroller(object):
    """walks dirs and moves old files into archive dirs per desired strategy"""

    def __init__(self, settings, printing=True, logging=True):

        # total number of files operated on
        self.filecount = 0
        # adding up to total bytes
        self.totalsize = 0
        self.tilde = settings.TILDE
        self.snooze = settings.SNOOZE
        # start-in directory
        self.startin = settings.STARTIN
        # default case insensitivity under Windows
        if os.name == 'nt':
            self.icase = True
            self.pattern = settings.PATTERN.lower().split('*')
            # list of excluded file fragments
            self.exclude_files = settings.EXCLUDE_FILES.lower().split()
            # list of excluded dirs - see also settings.SKIPFLAG
            self.exclude_dirs = settings.EXCLUDE_DIRS.lower().split()
        else:
            self.icase = False
            self.pattern = settings.PATTERN.split('*')
            self.exclude_files = settings.EXCLUDE_FILES.split()
            self.exclude_dirs = settings.EXCLUDE_DIRS.split()
        # shorten == True means to omit path/to/ startin,
        # False means to use entire startin sans leading os.path.sep
        self.shorten = settings.SHORTEN
        # do the shortening work here - it doesn't take long
        bits = os.path.split(settings.STARTIN)
        self.startin_base = bits[0]
        self.startin_dir = bits[1]
        # establish the one true base time for the entire operation
        self.now = time.time()
        # files older than cutoffdays (can be a decimal) are candidates
        self.cutoffdays = float(settings.CUTOFF)
        # the user's days converted to seconds
        self.cutoffsecs = float(settings.CUTOFF * 24 * 60 * 60)
        # convert an absolute number into a file-relative age as of now
        self.filecutoff = float(self.now - self.cutoffsecs)
        # detect created, modified or accessed times
        self.detect = settings.DETECT.lower()
        # destination dir upon which to graft the startin tree of old files
        # or maybe a symbolic 'year' or sub-year' destination
        self.destination = settings.DESTINATION
        # action is report, copy, move etc
        self.action = settings.ACTION.lower()
        # cleanup == True means get rid of temporary backup files
        self.cleanup = settings.CLEANUP
        # skip flag is a file of this name (skipthis.dir) left in a dir
        self.skipflag = settings.SKIPFLAG
        # which exclusion method to use with settings.SKIPFLAG
        self.skipsilent = settings.SKIPSILENT
        # currently settings.conf in cwd - it might be different in future
        self.config = settings.CONFIG
        # full path + config filename to write out the settings.conf in destin
        self.settings_used = settings.SETTINGS_USED
        # full path to logfile
        self.logname = settings.LOGNAME
        # True or False
        self.overwrite_log = settings.OVERWRITE_LOG
        # True is horrible for unit testing so set it False there
        self.logging = logging
        # printing == True means output to screen as well as to the log
        # True is horrible for unit testing so set it False there
        self.printing = printing
        # keep adding errors here
        self.failed = errorheader
        # keep count of errors here
        self.errors = 0
        # start the cpu clock for this run to get total elapsed time later
        time.clock()
        # for the log we need a commencement date-time
        dt = self.datestamp(time.localtime)
        run = 'Commenced on %s-%s-%s at %s:%s:%s' % \
              (dt[2], dt[1], dt[0], dt[3], dt[4], dt[5])
        # now open logfile and write the initial settings info
        if self.overwrite_log:
            omode = 'w'
            bar = ''
        else:
            omode = 'a'
            bar = '%s%s- - - - - - - - - - - - - - - - - - - - - - -%s' % (os.linesep, os.linesep, os.linesep)
        if self.logging:
            self.log = open(self.logname, omode)
        else:
            self.log = ''
        startinerr = '%s - start in folder %s' % (os.linesep, self.startin)
        if not os.path.isdir(self.startin):
            startinerr = '%s - %s is not a valid STARTIN directory' % (os.linesep, self.startin)
        msg = bar + 'Actions based on settings ...'+\
        startinerr +\
        '\n - cutoff of ' + str(self.cutoffdays) + ' days for '+\
        '\n - file ' + self.detect + ' times'+\
        '\n - action is ' + self.action +\
        '\n - cleanup is ' + str(self.cleanup) +\
        '\n - destination ' + self.destination +\
        '\n' + run
        self.logprint(msg)



    def _backup(self, dest):
        """create a backup of a destination file before overwriting it and
        send a message to the caller to say what happened - for the log
        """
        bak = gone2 = ''
        # check to see if dest exists
        if os.path.isfile(dest):
            # prepare the notification
            gone2 = ' +and+ %s overwritten' % dest
            # get rid of any previous backup (unlikely)
            bak = dest + self.tilde
            try:
                if os.path.isfile(bak):
                    os.remove(bak)
                os.rename(dest, bak)
            except (IOError, OSError) as e:
                self._errlog('%s %s%s' % (e, dest, os.linesep))
        return gone2

    def _cleanup(self, dest):
        """called every time but does nothing unless cleanup == True
        """
        if self.cleanup:
            bak = dest + self.tilde
            try:
                if os.path.isfile(bak):
                    os.remove(bak)
            except (IOError, OSError) as e:
                self._errlog('%s %s%s' % (e, bak, os.linesep))

    def _copyover(self, pathname, dest):
        """only called by take_action() if action is copy-overwrite.
        First backup any dest file and get the notification that the
        dest "was" (actually "is about to be") overwritten - if it was
        there already. Then copy it cleanly to the dest and send back
        the combined log messages.
        """
        # back it up if it is there already
        gone2 = self._backup(dest)
        # now we have an uncluttered destination
        # and the copy/move can't fail
        try:
            shutil.copy2(pathname, dest)
            self._increment(dest)
            gone = '%s --> copied --> %s' % (pathname, dest)
            return gone + gone2
        except (IOError, OSError) as e:
            self._errlog('%s %s%s' % (e, dest, os.linesep))
        return gone2

    def datestamp(self, func=None):
        """we need this to re-execute with the now current time every time
        we want a new log entry.
        """
        if func is None:
            func = time.localtime
        dt = list(func())
        # dt[3] hours dt[4] minutes dt[5] seconds all need to be formatted
        dt[3] = '%02d' % dt[3]  # with a leading zero if less then 10
        dt[4] = '%02d' % dt[4]
        dt[5] = '%02d' % dt[5]
        return dt

    def _errlog(self, err):
        self.failed += err
        # also keep the error in correct log sequence
        self.logprint(err)
        self.errors += 1

    def _increment(self, dest):
        # increment the file count
        self.filecount += 1
        # increment the total file size bytes copied/moved
        fil = os.stat(dest)
        sz = fil.st_size
        self.totalsize += sz

    def _move(self, pathname, dest):
        """only called if action is move
        """
        # get an extra bit of log message or blank
        gone2 = self._backup(dest)
        # now we have an uncluttered destination
        # and the copy/move won't fail
        try:
            # if this fails, the orig doesn't move - OSError exception
            os.rename(pathname, dest)
            self._increment(dest)
            gone = '%s --> moved --> %s' % (pathname, dest)
            return gone + gone2
        except (IOError, OSError) as e:
            self._errlog('%s %s%s' % (e, dest, os.linesep))
        return gone2

    def check_year_dir(self, item):
        """return a zero or a year integer """
        if self.destination == settings.SUBYEAR or \
           self.destination == settings.YEAR :
            try:
                return int(item)
            except ValueError:
                pass
        return 0

    def comma_format(self, tot=None):
        """there is probably a Python string function to do this"""
        if tot is None:
            tot = self.totalsize
        strtot = '%s' % tot
        revtot = commatot = outptot = ''
        # first reverse the digits
        for digit in strtot:
            revtot = digit + revtot
        # now insert commas ...
        ith = endth = 0
        for digit in revtot:
            commatot += digit
            ith += 1
            endth += 1
            # ... every three digits but not if it is the last one
            if ith == 3:
                ith = 0
                if endth < len(revtot): commatot += ','
        # now un-reverse for the output total
        for digit in commatot:
            outptot = digit + outptot
        return outptot

    def construct_dest(self, pathname):
        """pathname is the path and filename of the chappie to be moved. So
        we split them and work with the path only to construct a valid dest
        path according to the DESTINATION setting. If any directories need
        to be created, do it with self.make_dir(). Finally, we re-attach the
        filename to end up with a complete destination /path/to/filename
        """
        # either year or sub-year or an entire new root
        pth, fil = os.path.split(pathname)
        if self.destination == settings.SUBYEAR or \
           self.destination == settings.YEAR :
            # self.destination is year-symbolic
            newpth = self.make_dir(pth, self.what_year(pathname))
        else:
            # self.destination isn't year-symbolic - it is pre-validated path
            # self.dest_suffix() builds the dest tree (possibly 'shorten'ed)
            newpth = os.path.join(self.destination, self.dest_suffix(pth))
            # first test to see if the new path exists
            if not os.path.isdir(newpth):
                self.make_dir(newpth)
        return os.path.join(newpth, fil)

    def dest_suffix(self, pth):
        """called by self.construct_dest() this is for creating a destination
        path by adding a suffix to an already valid dest base. pth passed
        in is the candidate file's /path/to. This may have a driveletter
        or UNC double backslash. This method needs to strip all that off
        and return a naked (and possibly 'shorten'ed) pth suffix ready
        for a os.path.join to the (non-symbolic) destination base path
        """
        if self.shorten:
            # left-chop the amount of startin_base
            # +1 chops off the slash as well
            trunc = pth[len(self.startin_base):]
            if trunc.startswith(os.path.sep):
                trunc = trunc[1:]
            return trunc
        else:
            # we need the entire path/to sans leading slashes
            if pth.startswith('\\\\'):
                return pth[2:]
            if (pth.startswith('\\') or pth.startswith('/')):
                return pth[1:]
            pthbits = pth.split(':')
            if len(pthbits) == 2:
                # must be Windows ... wonder if a protocol://path/to works?
                # omit pthbits[0] - ie the drive letter and use pthbits[1]
                # and slice off the backslash too so we can use os.path.join
                pth = pthbits[1][1:]
        return pth

    def dirs_in_root(self, xdir=None):
        """When doing year moves, we want to skip directories with names
        like years otherwise we would have a hall of mirrors and go mad!
        We also want to exclude any exclude_dirs and return a sorted list
        of ordinary looking non-excluded directories contained in xdir
        """
        if xdir is None:
            xdir = self.startin
        dirs = list()
        for item in os.listdir(xdir):
            # includes files but we only want fully qualified dirs
            pathitem = xdir + os.path.sep + item
            if os.path.isdir(pathitem):
                x = self.check_year_dir(item) # not itemq
                # check_year_dir returns 0 or 2009 etc
                if x == 0: # not a year directory
                    # check for settings exclusions
                    if not self.is_excluded_dir(pathitem):
                        dirs.append(pathitem)
        dirs.sort()
        return dirs

    def files_in_dir(self, xdir):
        """list the non-excluded files in a given xdir"""
        files = list()
        for item in os.listdir(xdir):
            # reconstruct and test to see if it is a file
            item = xdir + os.path.sep + item
            if os.path.isfile(item):
                if not self.is_excluded_file(item):
                    # item is a full pathname
                    files.append(item)
        files.sort()
        return files

    def is_candidate(self, pathname):
        """the heart of filemov. Returns True if this file fits the spec.
        Also returns the actual date used of the file so it can be logged
        A file older than cutoff means (now - file-age) > cutoffsecs
        """
        # throwaway ddate if not a candidate - used for unit tests
        ddate = '1-1-1111'
        try:
            if self.detect == settings.ACCESSED:
                xtime = os.path.getatime(pathname)
                candidate = (self.now - xtime) > self.cutoffsecs
            elif self.detect == settings.MODIFIED:
                xtime = os.path.getmtime(pathname)
                candidate = (self.now - xtime) > self.cutoffsecs
            # need to investigate Linux ctime
            elif self.detect == settings.CREATED:
                xtime = os.path.getctime(pathname)
                candidate = (self.now - xtime) > self.cutoffsecs
            if candidate:
                ddate = self.secs2date(xtime)
        except Exception as e:
            err = '%s %s%s' % (e, pathname, os.linesep)
            if 'too long' in err:
                self.truncate_name(pathname)
            self._errlog(err)
            if not self.logging:
                # must be testing so we want to see this
                print('\n562 filemov.py\n%s' % err)
            candidate = False
        return candidate, ddate

    def truncate(self, pathname):
        pass

    def is_excluded_dir(self, pathitem):
        # for simplicity this is a case-insensitive test
        # needs to be enhanced for Linux one day - with a switch
        if self.icase:
            pathitem = pathitem.lower()
        for excldir in self.exclude_dirs:
            if pathitem.find(excldir) >= 0:
                return EXCLUDED
        return INCLUDED

    def fitspattern(self, fname):
        """If there is a pattern see if this fname fits. See __init__()
        Called only by is_excluded_file()
        """
        ok = True
        for bit in self.pattern:
            if len(bit) > 0:
                ok = ok and (fname.find(bit) >= 0)
        return ok

    def is_excluded_file(self, fileitem):
        """With no self.pattern fitspattern() is always True
        Called by files_in_dir"""
        if self.icase:
            fileitem = fileitem.lower()
        if self.fitspattern(fileitem):
            for exclfile in self.exclude_files:
                if fileitem.find(exclfile) > -1:
                    return EXCLUDED
        else:
            return EXCLUDED
        return INCLUDED

    def logprint(self, msg):
        """ append newline to write(msg) """
        if self.printing:
            # TODO -   print("%s" % e, file=sys.stderr)
            print("%s" % msg, file=sys.stdout)
        msg = str(msg) + os.linesep
        if self.logging:
            try:
                self.log.write(msg)
            except Exception:
                print("%s" % msg, file=sys.stderr)


    def make_dir(self, newpth, yr=None):
        if yr is not None:
            newpth = os.path.join(newpth, yr)
        if not os.path.isdir(newpth):
            # makedirs throws OSError if the directory exists
            if self.action != 'report':
                try:
                    os.makedirs(newpth)
                    if os.path.isdir(newpth):
                        return newpth
                    else:
                        return None
                except OSError as e:
                    self._errlog('%s %s%s' % (e, newpth, os.linesep))

        return newpth

    def remove_empty_folders(self):
        """ no unit tests for this - it is just Python """
        for root, dirnames, filenames in os.walk(self.startin, topdown=False):
            for dname in dirnames:
                dirname = os.path.join(root, dname)
                if len(os.listdir(dirname)) == 0:
                    try:
                        os.rmdir(dirname)
                        self.logprint('removing %s which is empty' % dirname)
                    except Exception as e:
                        self._errlog('%s%sproblem removing %s' % (e, os.linesep, dirname))

    def secs2date(self, seconds='fail', mins=None, secs=None):
        """If the user wants really accurate file dates she can call this with
        secs=True or less accurately mins=True. The default is date only.
        Returns weird if seconds == 'fail' or is None
        """
        try:
            d = time.localtime(seconds)
            if secs:
                return '%s-%s-%s %s:%s:%s' % (d.tm_mday, d.tm_mon, d.tm_year,
                                              '%02d' % d.tm_hour,
                                              '%02d' % d.tm_min,
                                              '%02d' % d.tm_sec,)
            elif mins:
                return '%s-%s-%s %s:%s' %  (d.tm_mday, d.tm_mon, d.tm_year,
                                              '%02d' % d.tm_hour,
                                              '%02d' % d.tm_min)
            else:
                return '%s-%s-%s' % (d.tm_mday, d.tm_mon, d.tm_year,)
        except Exception:
            # we have discovered real odd Windows files without dates!
            weird = 'No %s date' % self.detect
            return weird

    def take_action(self, pathname, ddate=''):
        """ is_candidate tests are already done - it remains to take the
        action specified in settings.conf and log the result

        """
        gone = ''
        dest = self.construct_dest(pathname)

        if self.action.startswith('move'):
            # don't want the file here - overwrite at the dest if necessary
            gone = self._move(pathname, dest) + ' ' + ddate

        elif self.action == 'copy-overwrite':
            # user obviously doesn't care if it is there already
            gone = self._copyover(pathname, dest) + ' ' + ddate

        elif self.action == 'copy':
            # do nothing if it exists - except log that fact
            if os.path.isfile(dest):
                gone = '<-- %s exists - not copied' % dest
            else:
                gone = self._copyover(pathname, dest) + ' ' + ddate

        elif self.action.startswith('report'):
            gone = '(Report only) %s %s' % (pathname, ddate)
            # report what might be done so use pathname rather than dest
            self._increment(pathname)
            if os.path.isfile(dest):
                gone = gone + ' +and+ %s exists ' % dest
        # finally remove the backup made during the process but not if
        # all we are doing is reporting!
        if not self.action.startswith('report'):
            self._cleanup(dest)
        return gone

    def visitfile(self, pathname):
        """called by self.sub_main() which discovers a non-excluded
        pathname (/path/to/file). This method checks if it is an age
        related candidate and if so, calls self.take_action()
        """
        candidate, ddate = self.is_candidate(pathname)
        if candidate:
            if self.snooze > 0.0000:
                time.sleep(self.snooze)
            self.logprint(self.take_action(pathname, ddate))

    def what_year(self, pathname):
        # element [0] is the year
        # only used when moving files into year dirs
        if self.detect == settings.ACCESSED:
            return str(time.localtime(os.path.getatime(pathname))[0])
        elif self.detect == settings.CREATED:
            return str(time.localtime(os.path.getctime(pathname))[0])
        elif self.detect == settings.MODIFIED:
            return str(time.localtime(os.path.getmtime(pathname))[0])


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def sub_main(self):
        """ Decision matrix for three different destination options
        being sub-year where all STARTIN's directories are pruned of old
        files and the clippings go into year-numbered sub-directories
        of each; then year where a single directory gets the same
        treatment; and thirdly, an actual destination folder somewhere
        to contain the tree rooted at STARTIN """

        if self.destination == settings.SUBYEAR :
            try:
                for dirname in self.dirs_in_root(None) :
                    for pathname in self.files_in_dir(dirname):
                        self.visitfile(pathname)
            except TypeError as e:
                self._errlog('%s%sNo directories found in %s' % (e, os.linesep, self.startin))
        elif self.destination == settings.YEAR :
            try:
                for pathname in self.files_in_dir(self.startin):
                    self.visitfile(pathname)
            except TypeError as e:
                self._errlog('%s%s%s directory not found' % (e, os.linesep, self.startin))
        else:
            # graft the tree onto a new root ie destination. dirpath is
            # the root for 2 lists: dirnames and filenames. os.walk
            # starts at the top (if topdown) and walks each dirname
            for dirpath, dirnames, filenames in os.walk(self.startin, topdown=True):
                # only stroll among permitted dirnames so look for 'skipthis.dir'
                if self.skipflag in filenames:
                    if self.skipsilent:
                        # empty this list of dirnames
                        dirnames[:] = []
                        continue
                        # on to next dirname without the call to logprint below
                    else:
                        # add it to the list of exclusions
                        if self.icase:
                            self.exclude_dirs.append(dirpath.lower())
                        else:
                            self.exclude_dirs.append(dirpath)
                # do we want this directory
                if self.is_excluded_dir(dirpath):
                    self.logprint('%s%s is excluded' % (os.linesep, dirpath))
                else:
                    # start grafting
                    dt = self.datestamp(time.localtime)
                    visited = ' visited on %s-%s-%s at %s:%s:%s' % \
                              (dt[2], dt[1], dt[0], dt[3], dt[4], dt[5])
                    self.logprint(os.linesep + dirpath + visited)
                    for fname in filenames:
                        if not self.is_excluded_file(fname):
                            self.visitfile(os.path.join(dirpath, fname))
            if self.action == 'move-remove-empty-folders':
                self.remove_empty_folders()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def main(self):
        """ initial check to see if there is a STARTIN then defer to a first
        level decision tree (sub-main) based on DESTINATION settings then
        when that is all finished, finalise the log and close it off
        """
        ok = True
        if os.path.isdir(self.startin):
            # run the entire program from go to whoa
            self.sub_main()
            # finished so report results
            sz = self.comma_format(self.totalsize)
            cnt = self.comma_format(self.filecount)
            msg = '\n%s %s files totalling %s bytes' % (self.action, cnt, sz)
            try:
                # finished now so let's leave some tilde evidence in case ...
                self.cleanup = False
                # copy the actual settings used to the destination root
                self._copyover(self.config, self.settings_used)
            except (IOError, OSError) as e:
                self._errlog('%s %s' % (e, self.settings_used))
        else:
            msg = os.linesep
            self.failed +=  '\n%s is not a valid STARTIN directory' % self.startin
            ok = False

        # append all the errors to the writen log so they all appear in one place
        if self.failed == errorheader:
            self.failed = '\nNo errors'
        else:
            # there must have been some errors so we need a footer
            self.failed += errorfooter
        self.logprint(self.failed)
        self.logprint('\n - errors detected = %s\n' % self.errors)

        # now finish off the log and close it
        #msg += '\n - excluded files ... \n\t%s' % '\n\t'.join(self.exclude_files)
        msg += '\nExcluded dirs ... \n\t%s' % '\n\t'.join(self.exclude_dirs)
        dt = self.datestamp(time.localtime)
        done = '\nFinished on %s-%s-%s at %s:%s:%s\n' % \
                  (dt[2], dt[1], dt[0], dt[3], dt[4], dt[5])
        msg += done
        msg += '%s seconds elapsed time' % time.clock()
        self.logprint(msg)
        if self.logging:
            self.log.close()
        return ok

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':

    import os, sys
    from settings import Settings

    def display_file(filename, action='open'):
        """Display the given filename in a separate application. On Windows
        platforms, the action parameter may be 'open' or 'print' and is passed
        to os.startfile() as an indication of what the separate application is
        to do with the file. On other platforms, it is ignored."""
        cmd = None
        if os.name == 'nt':
            os.startfile(filename, action)
        elif os.name == 'posix':
            if sys.platform == 'darwin':
                cmd = 'open'
            elif filename.lower()[-4:] in ['.xls', '.doc', '.ppt',
                                           '.csv', '.odt', '.ods', '.odp',
                                           'docx', 'xlsx', 'pptx',
                                          ]:
                cmd = 'soffice'
            elif filename.lower()[-4:] == '.pdf':
                cmd = 'evince'
            else:
                cmd = 'gedit'
            try:
                import subprocess
                subprocess.call([cmd, filename])
            except Exception as e:
                import traceback
                print('Failed to display %s: %s\n%s' % (filename, e,
                                                        traceback.format_exc()))

    args = sys.argv
    cmdline = '\nCommand line = %s\n' % ' '.join(args)

    # if ./settings.conf doesn't exist settings.py creates it
    settingsfile = os.path.join(os.getcwd(), 'settings.conf')

    if '-s' in args:
        try:
            # if settingsfile doesn't exist settings.py creates it
            settingsfile = args[args.index('-s') + 1]
        except Exception as e:
            print("Settings file %s" % e, file=sys.stderr)
            ok = False

    # get the settingsfile into the flow
    settings = Settings(settingsfile)

    if '-q' in args:
        obj = Stroller(settings, printing=False)
        obj.logprint(cmdline)
        obj.main()

    else:
        import subprocess
        obj = Stroller(settings, printing=True)
        obj.logprint(cmdline)
        if obj.main():
            if os.name == 'nt':
                ed = 'notepad.exe'
            else:
                ed = 'nano'
            # display the log
            cmd = '%s' % obj.logname
            #cmd = '%s %s' % (ed, obj.logname)
            subprocess.Popen(cmd, shell=True).wait()
            # and the settings
            cmd = '%s' % obj.settings_used
            #cmd = '%s settings.conf' % ed
            subprocess.Popen(cmd, shell=True).wait()

