#! /usr/bin/python

"""
The unittests here need a directory tree structure with a bunch of files to
move around and confirm expected results as tests.

The expected *development* directory structure is ...

envs---\
       |______filemov---\
       |                |_____distrib
       |                |_____doc
       |                |_____test_bak (contains test tree from test_bak.zip)
       |                |_____filemov---\
       |                |__init__.py    |
       |                |MANIFEST.py    |
       |                |readme.txt     |
       |                |setup.py       |
       |                |test_bak.zip   |
       |                                |_____doc
       |                                |_____test------\
       |                                |__init__.py    |
       |                                |filemov.py     |
       |                                |settings.py    |
       |                                                |____log
       |                                                |____testfiles
       |                                                |__init__.py
       |                                                |test_filemov.py
       |______ otherproject
       |______ and so on

The testfiles directory contains test_bak.zip. This zip contains a tree of
directories and files like this ...

test_bak.zip---\
               |____test_bak---\
                               |____test_files---\
                                                 |____folderx1 (more nested)
                                                 |____foldery1  (more nested)
                                                 |____folderz1  (more nested)
                                                 |00readme.txt
                                                 |adapter.ru.txt
                                                 | many more files

Copy the test_bak folder from test_bak.zip as indicated above.

There needs to be a RAWROOT location which contains the test_bak directory
from test_bak.zip (wherever that zip may be located).

The setup (Setup class) section below will copy the test_files directory to
RAWROOT from RAWROOT/test_bak (deleting test_files if it exists)

Be aware that access times and creation times might require that you
set the clock back to a suitable date when copying files. Alternatively
you can choose existing files with suitable access/creation dates.

Some of these unit tests will need to be edited in order to make the
test file ages (in days) relevant to the date on which you run them.

Some prepared test files to suit these tests ...

http://svn.climate.com.au/repos/pysrc/gpl3/test_bak.zip

Output from most unit tests goes to RAWROOT/test and RAWROOT/testx

All the weird uppercase bits and pieces are necessary because we have to
test different destinations made up out of path components as well as cater
for Windows case insensitivity and Linux case sensitivity.

Other in/output is based on UNC paths which you will have to work out.
"""

import os, sys, unittest, time, shutil
# increment pst until it brings the date checks back into range
from datetime import date
pst = date.toordinal(date.today()) - date.toordinal(date(2010, 1, 1))

# find the pathname of the directory immediately above this one
appdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
# appdir contains filemov.py so for the imports we need it in sys.path
sys.path.insert(0, appdir)
#print('\nsys.path = %s\n' % sys.path)

try:
    from filemov import Stroller
    from settings import *
except ImportError:
    raise

print('\npast = %s days ago!\n' % pst)

# edit RAWROOT and DRIVE = '' to suit your platform
win = (os.name == 'nt')

# we want a RAWROOT which sits above filemov in the fs which means
# two levels above this directory
# NOTE: must change to this dir for cwd to make sense

TESTLOG = os.path.join(os.getcwd(), 'test.log')
if os.path.isfile(TESTLOG):
    os.remove(TESTLOG)
OVERLOG = False
dd = time.localtime()
ddate = '%02d-%02d-%02d' % (dd.tm_year, dd.tm_mon, dd.tm_mday)
logname = 'filemov.log'

# first split gives ../envs/filemov/filemov
testroot = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
# second split gives ../envs/filemov
RAWROOT = os.path.split(testroot)[0]
DESTDIR = os.path.join(RAWROOT, 'test')     # ~/envs/test
RAWDEST = os.path.splitdrive(DESTDIR)[1]    # test
NETDIR = 'K:\\'

# the "repo" for a set of nicely aged test files
# ~/envs/test_bak/test_files
TESTBAK = DESTDIR + '_bak' + os.path.sep + 'test_files'

FILESUFFIX = '_files'
TESTDIR = DESTDIR + FILESUFFIX  # ~/gpl3/test_files
print("""121 test_filemov.py

RAWROOT    = %s (root dir for test_files)
DESTDIR    = %s (destination for copied test files)
RAWDEST    = %s (DESTDIR without the drive letter)
NETDIR     = %s (drive letter or UNC or Linux host)
TESTBAK    = %s (contains test files tree)
FILESUFFIX = %s (part of TESTDIR directory name)
TESTDIR    = %s (test tree)

Delays are due to the test tree being re-copied

IMPORTANT - After tests run, delete test conf files (See test.bat)
""" % (RAWROOT,DESTDIR,RAWDEST,NETDIR,TESTBAK,FILESUFFIX,TESTDIR))

def remtree(pth):
    if os.path.isdir(pth):
        for dirpath, dirnames, filenames in os.walk(pth, topdown=False):
            for fname in filenames:
                os.remove(os.path.join(dirpath, fname))
            for directory in dirnames:
                os.rmdir(os.path.join(dirpath, directory))
        os.rmdir(pth)


class Setup(object):

    def __init__(self, line, top=TESTDIR, dest=DESTDIR, bak=TESTBAK):
        # top is the dir where the tree to be walked is rooted
        # top='gpl3/test_files', dest='gpl3/test'
        self.top = top
        self.dest = dest
        self.bak = bak
        #print("\n154 test_filemov.py Replacing test files - called from %s" % line)

    def replace_test_files(self):
        if os.path.isdir(self.top):
            remtree(self.top)

        if os.path.isdir(self.dest):
            remtree(self.dest)

        if os.path.isdir('%sx'% self.dest):
            remtree('%sx'% self.dest)

        if os.path.isdir('%sy'% self.dest):
            remtree('%sy'% self.dest)

        shutil.copytree(self.bak, self.top)


class TestFilemov(unittest.TestCase):
    """
    1. create a settings object and adjust any settings args

    def __init__(self, settingsfile=CONFIG,
        # following args are only used by test_filemov although in future
        # we might provide some cmdline args which would use these too.
                        startin=None,
                         pattern=None,
                          shorten=None,
                           cutoff=None,
                            detect=None,
                             destination=None,
                              action=None,
                               cleanup=None,
                                exclude_files=None,
                                 exclude_dirs=None,
                                  skipsilent=None,
                                   logname=None,
                                    overwrite_log=None,
                                     snooze=None,
                                     ):

    2. create a filemov object and pass in the settings object

    tsto = Stroller(settings, printing=False, logging=False)

    """
    def test_wildcard_ru_68(self):
        """ 68
        """
        wild = '*.ru.*'
        testdir = TESTDIR
        settings = Settings(startin=testdir,
                                pattern=wild,)
        tsto = Stroller(settings, printing=False, logging=False)
        flist = tsto.files_in_dir(testdir)
        expected = 3
        self.assertEqual(len(flist), expected)


    def test_wildcard_xyz_67(self):
        """ 67
        """
        wild = '*.xyz'
        testdir = TESTDIR
        settings = Settings(startin=testdir,
                                pattern=wild,)
        tsto = Stroller(settings, printing=False, logging=False)

        flist = tsto.files_in_dir(testdir)
        expected = 0
        self.assertEqual(len(flist), expected)

    def test_wildcard_msg_66(self):
        """ 66
        """
        wild = 'msg*.txt'
        testdir = TESTDIR
        settings = Settings(startin=testdir,
                                pattern=wild,)
        tsto = Stroller(settings, printing=False, logging=False)

        flist = tsto.files_in_dir(testdir)
        expected = 45
        self.assertEqual(len(flist), expected)


    def test_dest_suffix_shorten65(self):
        """ 65
        rev 0.7.1 2626  md  27 apr 2010 - repaired dest_suffix bug which was
                    chopping off the leading character if shortening a
                    windows root dir. See unit test #65
        """
        drive, testdir = os.path.splitdrive(TESTDIR)
        expected = 'test_files'
        settings = Settings(startin=testdir,
                                shorten=True,)
        tsto = Stroller(settings, printing=False, logging=False)

        result = tsto.dest_suffix(testdir)
        self.assertEqual(result, expected)


    def test_fitspattern_64(self):
        """ 64 test that msg* retrieves all the msg_xx.txt files """
        settings = Settings(pattern='msg*02*txt',)
        tsto = Stroller(settings, printing=False, logging=False)

        testfile = 'xyz_msg_gdgdgdg02gsgsg.txt'
        fits = tsto.fitspattern(testfile)
        self.assertEqual(fits, True)

    def test_fitspattern_true(self):
        """ 63 test that msg* retrieves all the msg_xx.txt files

        We need to know where to get the files from ...
        if ~/gpl3/test_files/folderx1 has 90+ files
        then copy the msg files to ~/gpl3/test/msgs


        """
        testid = '63-228'
        destdir = os.path.join(DESTDIR + '63', 'msgs')
        testdir = TESTDIR
        settings = Settings(pattern = 'msg*',
                                destination = destdir,
                                shorten = True,
                                cutoff = 0,
                                #action = 'copy',
                                logname = TESTLOG + testid,)
        tsto = Stroller(settings, printing=False, logging=False)
        expected = 45
        tsto.sub_main()
        files = tsto.files_in_dir(testdir)
        #settings.printsettings(testid)
        self.assertEqual(len(files), expected)

    def test_omitted_dirs_false1(self):
        """62 test that folderzy3 doesn't get copied - it contains the flag file skipthis.dir"""

        # startin dir
        testdir = os.path.join(TESTDIR, 'foldery1')
        # this is where skipthis.dir lives (from test_bak/test_files/)
        testflag = os.path.join(testdir, 'folderzy3', SKIPFLAG)

        # destination - keep results separate in RAWROOT+testx
        destdir = DESTDIR + 'x'
        # here are some paths based on testx
        result2 = os.path.join(destdir, 'foldery1', 'folderzy2')
        # result3 should never be copied/moved because it contains SKIPFLAG
        result3 = os.path.join(destdir, 'foldery1', 'folderzy3')
        # C:\users\miked\py\gpl3\test_files\foldery1\folderzy2\folderx1
        result4 = os.path.join(result2, 'folderx1')
        # C:\users\miked\py\gpl3\test_files\foldery1\folderzy2\folderx1\folderyx1
        result5 = os.path.join(result4, 'folderyx1')
        # C:\users\miked\py\gpl3\test_files\foldery1\folderzy2\folderx1\folderyx1\folderzy2
        result6 = os.path.join(result5, 'folderzy2')
        # C:\users\miked\py\gpl3\test_files\foldery1\folderzy2\folderz1\msg_01.txt
        result7 = os.path.join(result5, 'folderzy3', 'msg_01.txt')
        # now create a test object
        settings = Settings(startin=testdir,
                                shorten=True,
                                cutoff= pst + 50,
                                detect=MODIFIED,
                                destination=destdir,
                                skipsilent=False,
                                action='copy',
                                cleanup=False,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        # ensure these do not exist just in case the previous run failed
        remtree(result2)
        remtree(result3)
        # now check that remtree has gotten rid of all these
        ok = os.path.isdir(result2)
        if ok: print('\n' + result2 + ' should not exist')
        self.assertEqual(ok, False)
        ok = os.path.isdir(result3)
        if ok: print('\n' + result3 + ' should not exist')
        self.assertEqual(ok, False)

        # these are below result2 and result3 and should not exist either
        ok = os.path.isdir(result4)
        if ok: print('\n' + result4 + ' should not exist')
        self.assertEqual(ok, False)
        ok = os.path.isdir(result5)
        if ok: print('\n' + result5 + ' should not exist')
        self.assertEqual(ok, False)

        # this should absolutely be there under all circs
        ok = os.path.isfile(testflag)
        if not ok: print('\n' + SKIPFLAG + ' is missing - test is invalid')
        self.assertEqual(ok, True)

        # now create the destin stuff using the whole shooting match
        tsto.main()

        # prove the directories exist in the testx destination
        ok = os.path.isdir(result2)
        if not ok: print('\n' + result2 + ' is missing')
        self.assertEqual(ok, True)

        # result3 should have been omitted - the main test
        ok = os.path.isdir(result3)
        if ok: print('\n' + result3 + ' should NOT exist')
        self.assertEqual(ok, False)
        #
        ok = os.path.isdir(result6)
        # C:\users\miked\py\gpl3\test_bak\test_files\foldery1\folderzy2\folderx1\folderyx1\folderzy2
        if not ok: print('\n' + result6 + ' is missing')
        self.assertEqual(ok, True)
        #
        ok = os.path.isfile(result7)
        if not ok: print('\n' + result7 + ' is missing')
        self.assertEqual(ok, True)
        #
        # restore for the other tests
        kickoff = Setup(371)
        kickoff.replace_test_files()

    #class test_filemov2(unittest.TestCase):
    def test_omitted_dirs_true(self):
        """ 61 test that folderzy3 doesn't get copied - it contains the flag file skipthis.dir """

        testdir = os.path.join(TESTDIR, 'foldery1')
        testflag = os.path.join(testdir, 'folderzy3', SKIPFLAG)
        destdir = DESTDIR + 'y'
        result2 = os.path.join(destdir, 'foldery1', 'folderzy2')
        # result3 should never be copied/moved because it contains SKIPFLAG
        result3 = os.path.join(destdir, 'foldery1', 'folderzy3')
        # C:\users\miked\py\gpl3\test_files\foldery1\folderzy2\folderx1
        result4 = os.path.join(result2, 'folderx1')
        # C:\users\miked\py\gpl3\test_files\foldery1\folderzy2\folderx1\folderyx1
        result5 = os.path.join(result4, 'folderyx1')
        # C:\users\miked\py\gpl3\test_files\foldery1\folderzy2\folderx1\folderyx1\folderzy2
        result6 = os.path.join(result5, 'folderzy2')
        # C:\users\miked\py\gpl3\test_files\foldery1\folderzy2\folderz1\msg_01.txt
        result7 = os.path.join(result5, 'folderzy3', 'msg_01.txt')
        # first clean out the destdir evidence from the previous run
        remtree(result2)
        remtree(result3)
        settings = Settings(startin=testdir,
                                shorten=True,
                                cutoff= pst + 50,
                                detect=MODIFIED,
                                destination=destdir,
                                skipsilent = True, # different path
                                action='copy',
                                cleanup=False,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        # first check that remtree has gotten rid of all these
        ok = os.path.isdir(result2)
        if ok: print('\n' + result2 + ' should not exist')
        self.assertEqual(ok, False)
        ok = os.path.isdir(result3)
        if ok: print('\n' + result3 + ' should not exist')
        self.assertEqual(ok, False)
        # these are below result2 and result3 and should not exist either
        ok = os.path.isdir(result4)
        if ok: print('\n' + result4 + ' should not exist')
        self.assertEqual(ok, False)
        ok = os.path.isdir(result5)
        if ok: print('\n' + result5 + ' should not exist')
        self.assertEqual(ok, False)
        # this should absolutely be there under all circs
        ok = os.path.isfile(testflag)
        if not ok: print('\n' + SKIPFLAG + ' is missing - test is invalid')
        self.assertEqual(ok, True)
        # now create the destin stuff
        tsto.main()
        #
        ok = os.path.isdir(result2)
        if not ok: print('\n' + result2 + ' is missing')
        self.assertEqual(ok, True)
        # result3 should have been omitted - the main test
        ok = os.path.isdir(result3)
        if ok: print('\n' + result3 + ' should NOT exist')
        self.assertEqual(ok, False)
        #
        ok = os.path.isdir(result6)
        # C:\users\miked\py\gpl3\test_bak\test_files\foldery1\folderzy2\folderx1\folderyx1\folderzy2
        if not ok: print('\n' + result6 + ' is missing')
        self.assertEqual(ok, True)
        #
        ok = os.path.isfile(result7)
        if not ok: print('\n' + result7 + ' is missing')
        self.assertEqual(ok, True)
        # restore for other tests
        kickoff = Setup(444)
        kickoff.replace_test_files()

    #class test_filemov3(unittest.TestCase):
    def test_construct_dest_shorten_unc63(self):
        """ 60 test_construct_dest_shorten
        when archiving files just use the last part of startin
        instead of the entire startin path sans drive letter"""
        testdir = r'\\pq5\samba\users\miked\py\gpl3\test_files'
        if os.path.isdir(testdir):
            destin = r'\\pq5\samba\users\miked\py\gpl3\test'
            settings = Settings(startin=testdir,
                                    shorten=True,
                                    destination=destin,
                                    overwrite_log=OVERLOG,
                                    logname=TESTLOG,)
            tsto = Stroller(settings, printing=False, logging=False)

            pathname = os.path.join(testdir, 'folderx1', 'folderyx2','namedcolors.txt')
            expected = os.path.join(destin, 'test_files','folderx1', 'folderyx2','namedcolors.txt')
            self.assertEqual(tsto.construct_dest(pathname), expected)

    def test_dest_suffix_shorten62(self):
        """ 59 left-truncate the path by the startin_base """
        testpth = os.path.join(TESTDIR, 'folderx1', 'folderyx1', 'msg01.txt')
        expected = os.path.join('test_files', 'folderx1', 'folderyx1', 'msg01.txt')
        settings = Settings(startin=TESTDIR,
                                shorten=True,)
        tsto = Stroller(settings, printing=False, logging=False)

        result = tsto.dest_suffix(testpth)
        self.assertEqual(result, expected)

    def test_dirs_in_root61(self):
        """ 58 test_dirs_in_root"""
        testdir = os.path.join(TESTDIR, 'foldery1', 'folderzy3')
        testin = os.path.join(testdir, SKIPFLAG)
        testoff = testin + 'xxx'
        settings = Settings(startin=testdir,)
        tsto = Stroller(settings, printing=False, logging=False)

        if os.path.isfile(testin):
            os.rename(testin, testoff)
        self.assertEqual(os.path.isfile(testin), False)
        self.assertEqual(os.path.isfile(testoff), True)
        dirlist = tsto.dirs_in_root()
        expected = 2
        os.rename(testoff, testin)
        self.assertEqual(os.path.isfile(testin), True)
        self.assertEqual(os.path.isfile(testoff), False)
        self.assertEqual(len(dirlist), expected)

    def test_dirs_in_root60(self):
        """ 57 test_dirs_in_root"""
        testdir = os.path.join(TESTDIR, r'folderx1')
        settings = Settings(startin=testdir,)
        tsto = Stroller(settings, printing=False, logging=False)

        dirlist = tsto.dirs_in_root()
        expected = 3
        if os.path.exists(os.path.join(TESTDIR, '2005')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2006')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2007')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2008')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2009')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2010')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2011')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2012')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2013')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2014')):
            expected += 1
        self.assertEqual(len(dirlist), expected)

    def test_files_in_dir59(self):
        """ 56 test_files_in_dir"""

        testdir = os.path.join(TESTDIR, 'folderx1')
        settings = Settings(startin=testdir,
                            exclude_files='filemov.log')
        tsto = Stroller(settings, printing=False, logging=False)

        flist = tsto.files_in_dir(testdir)
        expected = 94
        self.assertEqual(len(flist), expected)
        self.assertEqual(os.path.split(flist[0])[1], '00readme.txt')
        self.assertEqual(os.path.split(flist[-1])[1], 'xlicense.txt')

    def test_datestamp52(self):
        """55 datestamp"""
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        ds = tsto.datestamp(None)
        exp = list(time.localtime())
        self.assertEqual(ds[0:2], exp[0:2])
        self.assertEqual([int(ds[3]), int(ds[4]), int(ds[5])], exp[3:6])
        self.assertEqual(ds[6:8], exp[6:8])

    def test_datestamp(self):
        """54 datestamp"""
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        def func(): return [2010, 2, 14, 8, 2, 7, 6, 45, 1]
        ds = tsto.datestamp(func)
        expected = [2010, 2, 14, '08', '02', '07', 6, 45, 1]
        self.assertEqual(ds, expected)

    def test_getlog_6(self):
        """ 53 getlog in settings """
        if win:
            conf_log = '%sxyz\\abc\\log\\%s' % (NETDIR, logname)
            dest = NETDIR
            expected = '%sxyz\\abc\\log\\%s_%s' % (NETDIR, ddate, logname)
        else:
            conf_log = '/var/log/filemov/' + logname
            dest = '/home/'
            expected = '/var/log/filemov/%s_%s' % (ddate, logname)
        startin = TESTDIR
        settings = Settings(startin=TESTDIR,
                            destination=dest,
                            logname=conf_log)
        self.assertEqual(settings.LOGNAME, expected)

    def test_getlog_5(self):
        """ 52 getlog in settings """
        if win:
            conf_log = '.' + os.path.sep + 'log' + os.path.sep + logname
            dest = NETDIR
            expected = '.' + os.path.sep + 'log' + os.path.sep + '%s_%s' % (ddate, logname)
        else:
            conf_log = './log/' + logname
            dest = '/home/'
            expected = './log/%s_%s' % (ddate, logname)

        startin = TESTDIR
        settings = Settings(startin=TESTDIR,
                            destination = dest,
                            logname=conf_log)
        self.assertEqual(settings.LOGNAME, expected)

    def test_getlog_4(self):
        """ 51 getlog in settings """
        conf_log = 'DESTINATION' + os.path.sep + logname
        if win:
            dest = NETDIR
        else:
            dest = '/home/'

        expected = dest + '%s_%s' % (ddate, logname)
        startin = TESTDIR
        settings = Settings(startin=TESTDIR,
                            destination = dest,
                            logname=conf_log)
        self.assertEqual(settings.LOGNAME, expected)

    def test_getlog_3(self):
        """ 50 getlog in settings """
        startin = TESTDIR
        dest = 'year'
        if win:
            conf_log = '%sxyz\\abc\\log\\%s' % (NETDIR, logname)
            expected = '%sxyz\\abc\\log\\%s_%s' % (NETDIR, ddate, logname)
        else:
            conf_log = '/var/log/filemov/' + logname
            expected = '/var/log/filemov/%s_%s' % (ddate, logname)

        settings = Settings(startin=TESTDIR,
                            destination = dest,
                            logname=conf_log)
        self.assertEqual(settings.LOGNAME, expected)


    def test_getlog_2(self):
        """ 49 getlog in settings
        Because logname has no path component it goes to getcwd"""
        conf_log = logname
        startin = TESTDIR
        dest = 'year'     # need DESTINATION in the logname to go to startin
        expected = os.path.join(os.getcwd(), '%s_%s' % (ddate, logname))
        settings = Settings(startin=TESTDIR,
                            destination = dest,
                            logname=conf_log)
        self.assertEqual(settings.LOGNAME, expected)

    def test_getlog_1(self):
        """ 48 getlog in settings """
        conf_log = 'DESTINATION' + os.path.sep + logname
        startin = TESTDIR
        dest = 'year'
        expected = startin + os.path.sep + '%s_%s' % (ddate, logname)
        settings = Settings(startin=TESTDIR,
                            destination = dest,
                            logname=conf_log)
        self.assertEqual(settings.LOGNAME, expected)

    def test_secs2date_none(self):
        """ 47 secs2date """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        expected = 'No modified date'
        out = tsto.secs2date()
        self.assertEqual(out, expected)

    def test_secs2date_none_accessed(self):
        """ 46 secs2date """
        settings = Settings(detect='accessed',)
        tsto = Stroller(settings, printing=False, logging=False)

        expected = 'No accessed date'
        out = tsto.secs2date()
        self.assertEqual(out, expected)

    def test_secs2date_mins(self):
        """ 45 secs2date """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        expected = '27-5-2009 13:04'
        out = tsto.secs2date(1243393444.5, True)
        self.assertEqual(out, expected)

    def test_secs2date_secs(self):
        """ 44 secs2date """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        expected = '27-5-2009 13:04:04'
        out = tsto.secs2date(1243393444.5, True, True)
        self.assertEqual(out, expected)

    def test_secs2date_date(self):
        """ 43 secs2date """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        expected = '27-5-2009'
        out = tsto.secs2date(1243393444.5)
        self.assertEqual(out, expected)

    def test_comma_format_41(self):
        """ 42 test_comma_format """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        inp = 12345
        expected = '12,345'
        out = tsto.comma_format(inp)
        self.assertEqual(out, expected)

    def test_comma_format_40(self):
        """ 41 test_comma_format """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        inp = 1234
        expected = '1,234'
        out = tsto.comma_format(inp)
        self.assertEqual(out, expected)

    def test_comma_format_39(self):
        """ 40 test_comma_format """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        inp = 123
        expected = '123'
        out = tsto.comma_format(inp)
        self.assertEqual(out, expected)

    def test_comma_format_38(self):
        """ 39 test_comma_format """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)
        inp = 12
        expected = '12'
        out = tsto.comma_format(inp)
        self.assertEqual(out, expected)

    def test_comma_format_2(self):
        """ 38 test_comma_format """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        inp = 12345678900
        expected = '12,345,678,900'
        out = tsto.comma_format(inp)
        self.assertEqual(out, expected)

    def test_comma_format_1(self):
        """ 37 test_comma_format """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        inp = 123456789000
        expected = '123,456,789,000'
        out = tsto.comma_format(inp)
        self.assertEqual(out, expected)

    def test_dest_suffix_shorten_2(self):
        """ 36 dest_suffix """
        testdir = r'\\pq5\samba\users\miked\py\gpl3\test_files'
        if os.path.isdir(testdir):
            sfx = r'test_files'
            destin = r'\\pq5\samba\users\miked\py\gpl3\test'
            settings = Settings(startin=testdir,
                                    shorten=True,
                                    destination=destin,
                                    overwrite_log=OVERLOG,
                                    logname=TESTLOG,)
            tsto = Stroller(settings, printing=False, logging=False)

            pathname = os.path.join(testdir, 'foldery1', 'folderzy2', 'namedcolors.txt')
            dest = os.path.join(destin, tsto.dest_suffix(pathname))
            expected = os.path.join(destin, sfx, 'foldery1', 'folderzy2', 'namedcolors.txt')
            self.assertEqual(dest, expected)

    def test_dest_suffix_shorten_unc(self):
        """ 35 dest_suffix unc """
        testdir = r'\\pq5\samba\users\miked\py\gpl3\test_files'
        if os.path.isdir(testdir):
            sfx = r'test_files'
            destin = r'\\pq5\samba\users\miked\py\gpl3\test'
            settings = Settings(startin=testdir,
                                    shorten=True,
                                    destination=destin,
                                    overwrite_log=OVERLOG,
                                    logname=TESTLOG,)
            tsto = Stroller(settings, printing=False, logging=False)

            pathname = os.path.join(testdir, 'namedcolors.txt')
            dest = os.path.join(destin, tsto.dest_suffix(pathname))
            expected = os.path.join(destin, sfx, 'namedcolors.txt')
            self.assertEqual(dest, expected)

    def test_unc_paths_no_shorten_unc(self):
        """ 34 test_unc_paths """
        testdir = r'\\pq5\samba\users\miked\py\gpl3\test_files'
        if os.path.isdir(testdir):
            destin = r'\\pq5\samba\users\miked\py\gpl3\test'
            settings = Settings(startin=testdir,
                                    destination=destin,
                                    shorten=False,
                                    overwrite_log=OVERLOG,
                                    logname=TESTLOG,)
            tsto = Stroller(settings, printing=False, logging=False)

            pathname = testdir + os.path.sep + 'namedcolors.txt'
            dest = tsto.construct_dest(pathname)
            expected = r'\\pq5\samba\users\miked\py\gpl3\test' + \
                        r'\pq5\samba\users\miked\py\gpl3\test_files\namedcolors.txt'
            self.assertEqual(dest, expected)

    def test_missing_startin_in_settings_conf(self):
        """ 33 test_missing_startin """
        settings = Settings(startin=r'C:\xyzzy',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        self.assertEqual(False, tsto.main())

    def test_cleanup_false(self):
        """ 32 test_cleanup_true """
        settings = Settings(startin=TESTDIR,
                                destination=DESTDIR,
                                action='copy-overwrite',
                                cleanup=False,
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = os.path.join(TESTDIR, 'help.txt')
        newfile = tsto.construct_dest(pathname)
        bakfile = newfile + settings.TILDE
        gone = tsto.take_action(pathname)
        self.assertNotEqual(gone, '')
        expected = DESTDIR + RAWDEST + FILESUFFIX + os.path.sep + 'help.txt'
        there = os.path.isfile(expected)
        self.assertEqual(there, True)
        self.assertEqual(newfile, expected)

        gone = tsto.take_action(pathname)
        self.assertNotEqual(gone, '')
        expected = DESTDIR + RAWDEST + FILESUFFIX + os.path.sep + 'help.txt~'
        there = os.path.isfile(expected)
        self.assertEqual(there, True)
        self.assertEqual(bakfile, expected)

    def test_cleanup_true(self):
        """ 31 test_cleanup_true """
        settings = Settings(startin=TESTDIR,
                                destination=DESTDIR,
                                action='copy-overwrite',
                                cleanup=True,
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = os.path.join(TESTDIR, 'extend.txt')
        newfile = tsto.construct_dest(pathname)
        bakfile = newfile + settings.TILDE
        gone = tsto.take_action(pathname)
        expected = DESTDIR + RAWDEST + FILESUFFIX + os.path.sep + 'extend.txt'
        there = os.path.isfile(expected)
        self.assertEqual(there, True)
        self.assertEqual(newfile, expected)
        self.assertNotEqual(gone, '')

        gone = tsto.take_action(pathname)
        expected = DESTDIR + RAWDEST + FILESUFFIX + os.path.sep + 'extend.txt~'
        there = os.path.isfile(expected)
        self.assertEqual(there, False)
        self.assertEqual(bakfile, expected)
        self.assertNotEqual(gone, '')


    def test_dest_suffix(self):
        """ 30 test_dest_suffix """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        pth = tsto.dest_suffix(DESTDIR)
        # chop off the leading slash [1:]
        expected = RAWDEST[1:]
        self.assertEqual(pth, expected)

    def test_is_excluded_file(self):
        """ 29 test_is_excluded_file """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + '.htaccess'
        excluded = tsto.is_excluded_file(pathname)
        expected = True
        self.assertEqual(excluded, expected)

    def test_is_excluded_dir(self):
        """ 28 test_is_excluded_dir """
        settings = Settings()
        tsto = Stroller(settings, printing=False, logging=False)

        pathitem = TESTDIR + os.path.sep + '.svn'
        excluded = tsto.is_excluded_dir(pathitem)
        expected = True
        self.assertEqual(excluded, expected)

    def test_construct_dest(self):
        """ 27 test_construct_dest also tests dest_suffix """
        settings = Settings(startin=TESTDIR,
                                destination=DESTDIR,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'adapter_new2.txt'
        dest = tsto.construct_dest(pathname)

        expected = DESTDIR + RAWDEST + FILESUFFIX + os.path.sep + 'adapter_new2.txt'
        self.assertEqual(dest, expected)

    def test_take_action_real_26(self):
        """ 26 test_take_action

        requires file replacement
        """
        settings = Settings(startin=TESTDIR,
                                destination=DESTDIR,
                                action='move',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'adapter_new2.txt'
        gone = tsto.take_action(pathname)
        expected = DESTDIR + RAWDEST + FILESUFFIX + os.path.sep + 'adapter_new2.txt'
        there = os.path.isfile(expected)
        self.assertEqual(there, True)
        self.assertNotEqual(gone, '')
        # move so move it back for next time
        try:
            if there:
                os.rename(expected, pathname)
        except Exception as e:
            print('26 failure to restore moved files\n%s' % e)

    def test_take_action_25(self):
        """ 25 test_take_action """
        settings = Settings(startin=TESTDIR,
                                destination='year',
                                action='move',
                                detect='modified',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'ieee754.txt'
        gone = tsto.take_action(pathname)
        expected = os.path.join(TESTDIR, '2008', 'ieee754.txt')
        there = os.path.isfile(expected)
        self.assertEqual(there, True)
        self.assertNotEqual(gone, '')
        # move so move it back for next time
        try:
            if there:
                os.rename(expected, pathname)
        except Exception as e:
            print('25 failure to restore moved files\n%s' % e)


    def test_take_action_24(self):
        """ 24 test_take_action modified move"""
        settings = Settings(startin=TESTDIR,
                                destination='year',
                                detect='modified',
                                action='move',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'credits.txt'
        gone = tsto.take_action(pathname)
        self.assertNotEqual(gone, '')
        expected = os.path.join(TESTDIR, '2006', 'credits.txt')
        there = os.path.isfile(expected)
        self.assertEqual(there, True)
        # move so move it back for next time
        try:
            if there:
                os.rename(expected, pathname)
        except Exception as e:
            print('24 failure to restore moved files\n%s' % e)


    def test_take_action_23(self):
        """ 23 test_take_action modified copy"""
        settings = Settings(startin=TESTDIR,
                                detect='modified',
                                destination='year',
                                action='copy',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'msg_01.txt'
        # we want files with mtimes smaller than filecutoff
        gone = tsto.take_action(pathname)
        self.assertNotEqual(gone, '')
        expected = os.path.join(TESTDIR, '2005', 'msg_01.txt')
        there = os.path.exists(expected)
        self.assertEqual(there, True)

    def test_take_action_22(self):
        """ 22 test_take_action mod copy 01"""
        settings = Settings(startin=TESTDIR,
                                destination='year',
                                detect='modified',
                                action='copy',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'msg_02.txt'
        gone = tsto.take_action(pathname)
        self.assertNotEqual(gone, '')
        expected = os.path.join(TESTDIR, '2005', 'msg_02.txt')
        self.assertEqual(os.path.isfile(expected), True)

    def test_take_action_21(self):
        """ 21 test_take_action """
        settings = Settings(startin=TESTDIR,
                                destination='sub-year',
                                action='move',
                                detect='modified',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'adapter_new.txt'
        gone = tsto.take_action(pathname)
        self.assertNotEqual(gone, '')
        expected = os.path.join(TESTDIR, '2009', 'adapter_new.txt')
        there = os.path.isfile(expected)
        self.assertEqual(there, True)
        # move so move it back for next time
        try:
            if there:
                os.rename(expected, pathname)
        except Exception as e:
            print('21 failure to restore moved files\n%s' % e)


    def test_take_action_20(self):
        """ 20 test_take_action modified move 04"""
        settings = Settings(startin=TESTDIR,
                                destination='sub-year',
                                action='move',
                                detect='modified',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'adapter.txt'
        gone = tsto.take_action(pathname)
        self.assertNotEqual(gone, '')
        expected = os.path.join(TESTDIR, '2007', 'adapter.txt')
        there = os.path.isfile(expected)
        self.assertEqual(there, True)
        # move so move it back for next time
        try:
            if there:
                os.rename(expected, pathname)
        except Exception as e:
            print('20 failure to restore moved files\n%s' % e)


    def test_take_action_19(self):
        """ 19 test_take_action modified copy 20"""
        settings = Settings(startin=TESTDIR,
                                destination='sub-year',
                                action='copy',
                                detect='modified',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'foo.txt'
        # we want files with mtimes smaller than filecutoff
        gone = tsto.take_action(pathname)
        self.assertNotEqual(gone, '')
        expected = os.path.join(TESTDIR, '2007', 'foo.txt')
        there = os.path.exists(expected)
        self.assertEqual(there, True)

    def test_take_action_18(self):
        """ 18 test_take_action mod copy 01"""
        settings = Settings(startin=TESTDIR,
                                destination='sub-year',
                                action='copy',
                                detect='modified',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'foodforthought.txt'
        gone = tsto.take_action(pathname)
        self.assertNotEqual(gone, '')
        expected = os.path.join(TESTDIR, '2007', 'foodforthought.txt')
        self.assertEqual(os.path.isfile(expected), True)


    def test_is_candidate_a65(self):
        """ 17 test_take_action accessed 65"""
        pathname = 'C:\\users\\miked\\py\\chemdata\\src\\2009.1\\__init__.py'
        if os.path.isfile(pathname):
            settings = Settings(startin=TESTDIR,
                                    cutoff=100 + pst,
                                    detect='accessed',
                                    overwrite_log=OVERLOG,
                                    logname=TESTLOG,)
            tsto = Stroller(settings, printing=False, logging=False)

            expected = (False, '1-1-1111')
            ok, dday = tsto.is_candidate(pathname)
            if ok:
                now = time.time()
                atime = os.path.getatime(pathname)
                cutoffsecs = tsto.filecutoff
                print('\nindex.txt \nctime in secs = ' + str(atime))
                print('filecutoff secs '+str(cutoffsecs))
                print('cutoff - atime  ' + str(cutoffsecs - atime))
                print('now - cutoff    '+str(now - cutoffsecs))
                print('now - ctime     '+str(now - atime))
                print('cutoffdays '+str(tsto.cutoffdays)+' = '+str(tsto.cutoffsecs)+' secs\n')
            self.assertEqual((ok, dday), expected)

    def test_is_candidate_a55(self):
        """ 16 test_take_action accessed a55"""
        pathname = 'C:\\users\\miked\\py\\chemdata\\src\\2009.1\\__init__.py'
        if os.path.isfile(pathname):
            settings = Settings(startin=TESTDIR,
                                    cutoff=float(75 + pst),
                                    detect='accessed',
                                    overwrite_log=OVERLOG,
                                    logname=TESTLOG,)
            tsto = Stroller(settings, printing=False, logging=False)

            expected = (True, '15-10-2009')
            ok, dday = tsto.is_candidate(pathname)
            if not ok:
                now = time.time()
                atime = os.path.getatime(pathname)
                cutoffsecs = tsto.filecutoff
                print('\nindex.txt \nctime in secs = ' + str(atime))
                print('filecutoff secs '+str(cutoffsecs))
                print('cutoff - atime  ' + str(cutoffsecs - atime))
                print('now - cutoff    '+str(now - cutoffsecs))
                print('now - ctime     '+str(now - atime))
                print('cutoffdays '+str(tsto.cutoffdays)+' = '+str(tsto.cutoffsecs)+' secs\n')
            self.assertEqual((ok, dday), expected)

    def test_is_candidate_c65(self):
        """ 15 test_take_action created 65"""
        settings = Settings(startin=TESTDIR,
                                cutoff=65 + pst,
                                detect='created',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'index.txt'
        expected = (False, '1-1-1111')
        ok, dday = tsto.is_candidate(pathname)
        self.assertEqual((ok, dday), expected)

    def test_is_candidate_c55(self):
        """ 14 test_take_action created c55"""
        settings = Settings(startin=TESTDIR,
                                cutoff=45 + pst,
                                detect='created',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTBAK + os.path.sep + 'index.txt'
        # we need a file actually created on the expected date
        # might need to set the clock back before copying/creating it.
        expected = (True, '27-5-2009')
        ok, dday = tsto.is_candidate(pathname)
        if not ok:
            now = tsto.now
            ctime = os.path.getctime(pathname)
            cutoffsecs = tsto.filecutoff
            print('\nindex.txt (created)\nctime in secs = ' + str(ctime))
            print('filecutoff secs '+str(cutoffsecs))
            print('cutoff - atime  ' + str(cutoffsecs - ctime))
            print('now - cutoff    '+str(now - cutoffsecs))
            print('# NOTE - now - ctime will be tiny if the test files have been recently moved')
            print('now - ctime     '+str(now - ctime))
            print('cutoffdays '+str(tsto.cutoffdays)+' = '+str(tsto.cutoffsecs)+' secs\n')
        self.assertEqual((ok, dday), expected)

    def test_is_candidate_2c55(self):
        """ 13 test_take_action created c55"""
        settings = Settings(startin=TESTDIR,
                                cutoff=45 + pst,
                                detect='created',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = os.path.join(TESTBAK, 'folderx1', 'folderyx2', 'index.txt')
        # we need a file actually created on the expected date
        # might need to set the clock back before copying/creating it.
        expected = (True, '27-5-2009')
        ok, dday = tsto.is_candidate(pathname)
        if not ok:
            now = tsto.now
            ctime = os.path.getctime(pathname)
            cutoffsecs = tsto.filecutoff
            print('\nindex.txt (created)\nctime in secs = ' + str(ctime))
            print('filecutoff secs '+str(cutoffsecs))
            print('cutoff - atime  ' + str(cutoffsecs - ctime))
            print('# NOTE - now - ctime will be tiny if the test files have been recently moved')
            print('now - cutoff    '+str(now - cutoffsecs))
            print('now - ctime     '+str(now - ctime))
            print('cutoffdays '+str(tsto.cutoffdays)+' = '+str(tsto.cutoffsecs)+' secs\n')
        self.assertEqual((ok, dday), expected)

    def test_is_candidate_m220(self):
        """ 12 test_is_candidate"""
        settings = Settings(startin=TESTDIR,
                                cutoff=250 + pst,
                                detect='modified',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'requires.txt'
        expected = (False, '1-1-1111')
        ok, dday = tsto.is_candidate(pathname)
        if ok:
            now = time.time()
            mtime = os.path.getmtime(pathname)
            cutoffsecs = tsto.filecutoff
            print('\nindex.txt \nmtime in secs = ' + str(mtime))
            print('filecutoff secs '+str(cutoffsecs))
            print('cutoff - mtime  ' + str(cutoffsecs - mtime))
            print('now - cutoff    '+str(now - cutoffsecs))
            print('now - ctime     '+str(now - mtime))
            print('cutoffdays '+str(tsto.cutoffdays)+' = '+str(tsto.cutoffsecs)+' secs\n')
        self.assertEqual((ok, dday), expected)

    def test_is_candidate_m210(self):
        """ 11 test_take_action modified 04"""
        testid = '11-1209'
        settings = Settings(startin=TESTDIR,
                                cutoff=210 + pst,
                                detect='modified',
                                overwrite_log=OVERLOG,
                                logname=TESTLOG + testid,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'requires.txt'
        expected = (True, '27-5-2009')
        ok, dday = tsto.is_candidate(pathname)
        #settings.printsettings(testid)
        self.assertEqual((ok, dday), expected)

    def test_check_year_dir_j(self):
        """ 10 test_check_year_dir_j"""
        if win:
            dest = NETDIR
        else:
            dest = '/home/'
        settings = Settings(startin=TESTDIR,
                                destination=dest,)
        tsto = Stroller(settings, printing=False, logging=False)

        item = '2005'
        expected = 0
        self.assertEqual(tsto.check_year_dir(item), expected)

    def test_check_year_dir_x(self):
        """ 9 test_check_year_dir_x"""
        settings = Settings(startin=TESTDIR,
                                destination='sub-year',)
        tsto = Stroller(settings, printing=False, logging=False)

        item = 'xyz'
        expected = 0
        self.assertEqual(tsto.check_year_dir(item), expected)

    def test_check_year_dir(self):
        """ 8 test_check_year_dir"""
        settings = Settings(startin=TESTDIR,
                            destination='sub-year',)
        tsto = Stroller(settings, printing=False, logging=False)

        item = '2005'
        expected = 2005
        self.assertEqual(tsto.check_year_dir(item), expected)

    def test_make_dir_false(self):
        """ 7 test_make_dir"""
        settings = Settings(startin=TESTDIR,
                                action='report',)
        tsto = Stroller(settings, printing=False, logging=False)

        yr = '2099'
        expected = TESTDIR + os.path.sep + yr
        if os.path.isdir(expected):
            os.rmdir(expected)
        self.assertEqual(os.path.isdir(expected), False)
        newpth = tsto.make_dir(TESTDIR, yr)
        self.assertEqual(newpth, expected)
        self.assertEqual(os.path.isdir(newpth), False)
        #os.rmdir(newpth) # clean up

    def test_make_dir_true(self):
        """ 6 test_make_dir"""
        settings = Settings(startin=TESTDIR,
                                action='report-make-folders',)
        tsto = Stroller(settings, printing=False, logging=False)

        yr = '2098'
        expected = TESTDIR + os.path.sep + yr
        if os.path.isdir(expected):
            os.rmdir(expected)
        self.assertEqual(os.path.isdir(expected), False)
        newpth = tsto.make_dir(TESTDIR, yr)
        self.assertEqual(newpth, expected)
        self.assertEqual(os.path.isdir(newpth), True)
        os.rmdir(newpth) # clean up

    def test_what_year(self):
        """ 5 test_what_year"""
        settings = Settings(startin=TESTDIR,
                                detect=MODIFIED,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'adapter.ru.txt'
        expected = '2009'
        yr = tsto.what_year(pathname)
        self.assertEqual(yr, expected)

    def test_not_is_candidate(self):
        """ 4 test_not_is_candidate"""
        settings = Settings(startin=TESTDIR,
                                cutoff=22 + pst,
                                detect=MODIFIED,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'newtstfile.txt'
        expected = (False, '1-1-1111')
        ok, dday = tsto.is_candidate(pathname)
        if ok:
            now = time.time()
            mtime = os.path.getmtime(pathname)
            cutoffsecs = tsto.filecutoff
            print('\n%s\nmtime in secs = %s' % (pathname, mtime))
            print('filecutoff secs '+str(cutoffsecs))
            print('cutoff - mtime  ' + str(cutoffsecs - mtime))
            print('now - cutoff    '+str(now - cutoffsecs))
            print('now - ctime     '+str(now - mtime))
            print('cutoffdays '+str(tsto.cutoffdays)+' = '+str(tsto.cutoffsecs)+' secs\n')
        self.assertEqual((ok, dday), expected)

    def test_is_candidate_600(self):
        """ 3 test_is_candidate"""
        testid = '3-1323'
        settings = Settings(startin=TESTDIR,
                                cutoff=600 + pst,
                                detect=MODIFIED,
                                logname=TESTLOG + testid,)
        tsto = Stroller(settings, printing=False, logging=False)

        pathname = TESTDIR + os.path.sep + 'oldfile.txt'
        expected = (True, '28-10-2005')
        ok, dday = tsto.is_candidate(pathname)
        #settings.printsettings(testid)
        self.assertEqual((ok, dday), expected)

    def test_files_in_dir(self):
        """ 2 test_files_in_dir"""
        settings = Settings(startin=TESTDIR,)
        tsto = Stroller(settings, printing=False, logging=False)

        tsto.exclude_files.append('filemov.log')
        flist = tsto.files_in_dir(TESTDIR)
        expected = 96
        self.assertEqual(len(flist), expected)
        self.assertEqual(os.path.split(flist[0])[1], '00readme.txt')
        self.assertEqual(os.path.split(flist[-1])[1], 'xlicense.txt')

    def test_dirs_in_root(self):
        """ 1 test_dirs_in_root"""
        settings = Settings(startin=TESTDIR,)
        tsto = Stroller(settings, printing=False, logging=False)
        dirlist = tsto.dirs_in_root()
        expected = 3
        self.assertEqual(len(dirlist), expected)
        if os.path.exists(os.path.join(TESTDIR, '2005')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2006')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2007')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2008')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2009')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2010')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2011')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2012')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2013')):
            expected += 1
        if os.path.exists(os.path.join(TESTDIR, '2014')):
            expected += 1
        self.assertEqual(len(dirlist), expected)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":

    kickoff = Setup(1420)
    kickoff.replace_test_files()
    unittest.main()


