"""mcm_wts.py - reads the wts_profile script and outputs the adjustments for shorts 2.0



"""
import os
shortspath = r'\\Mcm_main_srv\SYS\PUBLIC\shorts'

#print(shortspath)

header = """REM  ***** miked for project Shorts ******* 2007
rem - If you are a member of administrators AND a member of other
rem - groups you get the other groups stuff but inserted into
rem - dirs named after the group. This lets administrators see
rem - what each user might be getting thanks to membership of
rem - that particular group. Non-admins get all their shortcuts
rem - directly in I:\Shorts folder no matter how many groups they
rem - are in. Only admins get a separate folder per group
rem -
rem - Mar 2011 miked changed give single batch file using environment
rem - variables and improved performance for WAN operations
rem -
rem - 2010 miked changed to account for central --> central.mcm
rem - replaced .o=central with .ou=central.o=mcm
rem -
rem - groups were relocated. This adjustment really needs to be
rem - refactored in future (post-NBN) so it works for *.mcm

REM Map an I: drive for the WTS user. CENTRAL USERS ALREADY HAVE I: DRIVE
rem - this needs to be refactored to ONLY map I: if the login context is central

IF LOGIN_CONTEXT<>"central"  and LOGIN_CONTEXT<>"central.mcm"  THEN BEGIN
  IF P_STATION="00145ED7EEEA"  then MAP ROOT I:=MCM_MAIN_SRV/DATA:WTSUSERS\%1
END

write "LOGIN_CONTEXT = " ; LOGIN_CONTEXT
write "LOGIN_ALIAS_CONTEXT = " ; LOGIN_ALIAS_CONTEXT

rem **** miked reserves V: for shorts groups directories ****

MAP ROOT V:=MCM_MAIN_SRV/DATA:groups

SET group_login="no"

rem ******************* edit nothing above ********************
rem ***********************************************************
"""

footer = """

rem ***********************************************************
rem ******************* edit nothing below ********************

IF %group_login" == "Yes" THEN BEGIN
  #\Mcm_main_srv\SYS\PUBLIC\shorts\group_login.bat
END

MAP DISPLAY ON
MAP ERRORS ON

EXIT

"""

# read wts_profile and gather all the group names for the batch file
groups = list()
wtsfile = r'C:\users\miked\py\gpl3\general\shorts\mcm_wts_groups.in'
unwanted = r'#\\Mcm_main_srv\SYS\PUBLIC\shorts\group_login.bat'
stars = '\nrem ***********************************************************\n'
nobelow = 'rem ******************* edit nothing below ********************\n'

with open(wtsfile, 'r') as fsock:
    for line in fsock:
        lin = line.lower().strip()
        if "if member of" in lin :
            bits = lin.split('=')
            if len(bits) > 1:
                # bits[1] should be the canonically qualified groupname
                group = bits[1].split('.')[0]
                # insert prior line to blank out the environment variable
                groups.append('SET ' + group + '=""\n')
                # now append the 'if member of' line as was
                groups.append(line)
                # consume the line
                line = ''
                # now append the environment var line
                groups.append('  SET ' + group + '="yes"\n')
                groups.append('  SET group_login="yes"\n')
            else:
                groups.append(line)

        if unwanted in line:
            continue

        groups.append(line)

middle = '\n'
for item in groups:
    middle += item

batfile = 'mcm_wts_groups.txt'

with open(batfile, 'w') as fsock:
    fsock.write(header.encode('utf-8'))
    fsock.write(middle.encode('utf-8'))
    fsock.write(footer.encode('utf-8'))


