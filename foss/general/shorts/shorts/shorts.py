longdesc = """shorts.exe (or shorts.py) reads all the directories in shortspath and rebuilds
group_login.bat"""

payload = 'payload_for_all_desktops'

longerdesc = """Correct shorts procedure
========================
1. create a novell security group

2. update the wts_profile.central.mcm script to include the new group

3. create a dir <shortspath>\<group> named to EXACTLY match the new group and
to contain the payload of files to be delivered to group members

4. Every time wts_profile changes as a result of an admin performing the above
three steps, shorts.exe needs to be run so that the group_login.bat exactly
complements the wts_profile login script.

Note A: There are two special sub-directories in <shortspath> which should
never be renamed: {payload} and payload_for_all_houses.

Note B: The contents of {payload} will be copied to all desktops
at every login if they don't already exist. There is a way to renew or remove
previously copied desktop files but it requires familiarity with DOS batch
file processing as follows:

    - find the appropriate point in this file for deleting something

    - insert a new line containing the DOS command you wish to execute

    - save this file. Deletions will begin as people login afresh

    - wait until all users are likely to have logged-in

    - either remove the inserted line or run shorts.exe again

Note C: The contents of payload_for_all_houses is a single self-extracting zip
file which should be emailed to each house. When executed, it will deliver
files as required in the houses. It is kept in the <shortspath> directory
purely for convenience because it too is a way of delivering payloads. There
is a way to renew the contents of a self-extracting zip file but it requires
familiarity with WinZip and the WinZip self-extractor utility.


Background
==========
Every login script for each local Novell server could set an environment
variable called "shortspath" to nominate the the correct shortspath - for
example ...

  SET shortspath="\\\\mcm_northern_srv\sys\PUBLIC\shorts"

... however, this implies a local shorts infrastructure which would require
maintenance and support. Better for everyone to run shorts from Central.

If the user is a member of wts_profile.central.mcm shortspath will be set as
follows:

  SET shortspath="\\\\mcm_main_srv\sys\PUBLIC\shorts"

... so that the Central shortspath will be used.

To prevent the wts_profile.central.mcm script from running, finish the local
login script with the Novell EXIT command.


What does wts_profile do at every login?
========================================
1. wts_profile.central.mcm creates the shortspath environment variable as
indicated above

2. wts_profile.central.mcm creates a non-blank environment var for every
group the user is in

3. wts_profile.central.mcm final command is <shortspath>\group_login.bat

4. wts_profile EXITs back to Novell - which finishes logging the user in.


What does goup_login.bat do at every login?
===========================================
1. It tests every group name it knows about and if it exists as a non-blank
environment var treats it as a hit and delivers the payload currently in the
<shortspath>/<sub-dir> with the same name as the group the user is in.

Note: If the user is in the Administrator group then all payloads due to being
in other Novell groups are delivered to group sub-directories in I:\shorts
instead of directly into I:\shorts. This is a convenience for Administrators
to more easily test the setting up of new groups and new payloads.

2. It copies the contents of <shortspath>\{payload} to every
user's desktop

3. It runs any extra commands inserted at appropriate places by administrators


How does shorts.exe work?
=========================
shorts.exe re-writes <shortspath>\group_login.bat.

shorts.exe needs to be manually executed after someone has made a change in
shorts. This might be a new group or removal of an old group.

It does not need to be run at any other time unless you wish to deliberately
re-create group_login.bat. This might be appropriate after editing it for
testing or removing inserted lines.

1. shorts.exe reads the %shortspath% environment variable to discover where
the group_login.bat file should be. Failing that, it defaults to ...

    \\\\Mcm_main_srv\sys\PUBLIC\shorts

2. It scans the directory names in %shortspath% to discover which groups
exist. This is why it is vital for admins to keep those directories EXACTLY
in step with groups listed in wts_profile.central.mcm

3. It uses those directory names to build group_login.bat from scratch
overwiting the previous version.

4. Everyone who logs in gets group_login.bat run for them by the Novell
login script mechanism which calls wts_profile.central.mcm

5. group_login.bat delivers the files and shortcuts allocated as payload
for all members of the groups concerned.

""".format(payload=payload)

comment = longerdesc

source = """Source:  Userid is 'public' with no password.
http://svn.pczen.com.au/repos/pysrc/gpl3/general/shorts/distrib/

Mike Dewhirst
0411 704 143
miked@dewhirst.com.au
"""

relnote = """shorts - see below for description
=======

Version    Build  Who   When/What
=================================
ver 0.1.1  2725   md    7-jun-2012  - Re-worked the commentary inserted into
                        group_login.bat for better accuracy and clarity. No
                        change to the code.

ver 0.1.0  2724   md    6-jun-2012  - D(ebug)-day for Win7. Graeme tracked down
                        a Windows 7 stupidity whereby ~ tilde in a dir name makes
                        Win7 barf. Renamed ~desktop to payload_for_all_desktops.
                        Change xcopy to copy for getting desktop contents across.

                        This is a backwards incompatible change due to adjusted
                        directory names removing the tilde dirs. There is likely
                        also to be further change to become properly compatible
                        with Win7 and simultaneously work with WinXP.

ver 0.0.6  2700   md    7-apr-2011  - Re-worked the last section of the output to
                        get everything in ~desktop and added more explanatory text.

ver 0.0.5  2697   md    5-apr-2011  - Re-worded the last section of the output
                        to provide a little guidance to users.

ver 0.0.4  2696   md    5-apr-2011  - adjusted to avoid directories beginning
                        with a tilde. Need a mechanism to skip other dirs.

ver 0.0.3  2695   md    5-apr-2011  - adjusted to avoid directories beginning
                        with a dot. It was picking up .svn directories.

ver 0.0.2  2693   md    30-mar-2011 - refactored to simplify it

ver 0.0.1  2688   md    28-mar-2011 - first written


Description
===========
%s

%s

%s

License
=======
Copyright (C) 2011 Mike Dewhirst

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

""" % (longdesc, comment, source)

__doc__ = relnote

import os
try:
    shortspath = os.environ['shortspath']
    if not os.path.isdir(shortspath):
        raise KeyError
except KeyError:
    # pleeeease guarantee that this dir exists
    shortspath = r'\\Mcm_main_srv\sys\PUBLIC\shorts'
    if os.environ['computername'] == 'DEV-WX':
        shortspath = r'C:\users\miked\py\gpl3\general\shorts\pq8nw\shorts'
        print(shortspath)


header = """@echo off
goto endcomment       DO NOT EDIT EXCEPT FOR TESTING

This file is recreated programmatically by running shorts.exe. This
should be done after any changes to WTS_PROFILE and the resulting changes
to sub-directories in ...

    {shortspath}

To get permanent changes adjust the program source prior to running it again.

{source}


{comment}

:endcomment

rem - Commands in this section run every time this file is executed

if not exist i:\shorts (mkdir i:\shorts > NUL)

::================================================================
rem - Commands in this middle section ONLY work when this batch file runs
rem - automatically at login. Nothing in this section works at other times.
""".format(shortspath=shortspath, comment=comment, source=source)

desktop = r'%USERPROFILE%\Desktop'

footer = """::================================================================
rem - This last section copies everything in desktop_payload to every user
rem - desktop provided the date on the file in desktop_payload is newer than
rem - the same file on users actual desktop (if using the xcopy line below).

rem - Anything in this section should(!) work every time this batch file runs.

rem - xcopy "{shortspath}\{payload}\*.*" "{desktop}" /D /S /C /I /H /R /Y /Z /Q /EXCLUDE:{shortspath}\exclude.svn > NUL
copy "{shortspath}\{payload}\*.*" "{desktop}" /Y

""".format(shortspath=shortspath, payload=payload, desktop=desktop)

groups = list()
for item in os.listdir(shortspath):
    dirpath = os.path.join(shortspath, item)
    if os.path.isdir(dirpath):
        if not item.startswith('.'):
            if not 'payload' in item:
                groups.append(item.lower())


admin = 'administrators'
try:
    # bring administrators to the top of the list
    x = groups.index(admin)
    #print('%s' % x)
    groups.insert(0, groups[x])
    del groups[x + 1]
except ValueError:
    pass

middle = '\nset admin=\n\n'
for item in groups:
    if not item == admin:
        middle += 'if not xx%admin% == xx ( set admin=\\' + item + ' )\n'
    middle += 'if not xx%' + item + '% == xx (' + '\n'
    middle += '  xcopy "' + shortspath + '\\' + item + '\\*.*" i:\\shorts%admin% '
    middle += '/D /S /C /I /H /R /Y /Z /Q /EXCLUDE:' + shortspath
    middle += '\\exclude.svn > NUL\n'
    # comment the next line to leave environment vars in place
    middle += '  set ' + item + '=\n'
    if item == admin:
        middle += '  set admin=yes\n'
    middle += ')\n\n'

batfile = os.path.join(shortspath, 'group_login.bat')

with open(batfile, 'w') as fsock:
    fsock.write(header.encode('utf-8'))
    fsock.write(middle.encode('utf-8'))
    fsock.write(footer.encode('utf-8'))


