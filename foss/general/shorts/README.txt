shorts - a Python program

shorts.exe (or shorts.py) reads all the directories in shortspath and rebuilds
group_login.bat

Howto

Correct shorts procedure
========================
1. create a novell security group

2. update the wts_profile.central.mcm script to include the new group

3. create a dir <shortspath>\<group> named to EXACTLY match the new group and
to contain the payload of files to be delivered to group members

4. Every time wts_profile changes as a result of an admin performing the above
three steps, shorts.exe needs to be run so that the group_login.bat exactly
complements the wts_profile login script.

Note A: There are two special sub-directories in <shortspath> which should
never be renamed: payload_for_all_desktops and payload_for_all_houses.

Note B: The contents of payload_for_all_desktops will be copied to all desktops
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

  SET shortspath="\\mcm_northern_srv\sys\PUBLIC\shorts"

... however, this implies a local shorts infrastructure which would require
maintenance and support. Better for everyone to run shorts from Central.

If the user is a member of wts_profile.central.mcm shortspath will be set as
follows:

  SET shortspath="\\mcm_main_srv\sys\PUBLIC\shorts"

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

2. It copies the contents of <shortspath>\payload_for_all_desktops to every
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

    \\Mcm_main_srv\sys\PUBLIC\shorts

2. It scans the directory names in %shortspath% to discover which groups
exist. This is why it is vital for admins to keep those directories EXACTLY
in step with groups listed in wts_profile.central.mcm

3. It uses those directory names to build group_login.bat from scratch
overwiting the previous version.

4. Everyone who logs in gets group_login.bat run for them by the Novell
login script mechanism which calls wts_profile.central.mcm

5. group_login.bat delivers the files and shortcuts allocated as payload
for all members of the groups concerned.



Source:  Userid is 'public' with no password.
http://svn.pczen.com.au/repos/pysrc/gpl3/general/shorts/distrib/

Mike Dewhirst
0411 704 143
miked@dewhirst.com.au
