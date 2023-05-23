# -*- coding: utf-8 -*-
# Copyright (c) 2011-2020 Climate Pty Ltd
# This is free software subject to the terms of the GNU AGPL v3
"""
getcreds returns secret info which should never be stored in a
repository. For example, username and password etc.

It requires a credsroot directory to already exist and also a project
sub-directory to contain text files holding the required secret
information. Other secret info would be in other project sub-dirs.

When called with project="xyz" and credsroot="/var/www/creds" (the
default), it joins them to discover credsdir in which it looks for
fname which contains the secret info. Otherwise, if you supply the
entire credsdir eg "/var/www/creds/xyz" it will use that instead.

Forward slashes always work on Windows in Python code. Otherwise
use doubled backslashes eg "\\var\\www\\creds\\xyz"

Each line of the named text file (fname) will be read into a list
with the first line in the zero'th element of the list ie creds[0]

In your code requiring credentials or other secret info for example:

from getcreds import getcreds
...
credslist = getcreds("db.host", project="xyz")
database_host = credslist[0]
database_port = credslist[1]
database_user = credslist[2]
database_pass = credslist[3]
# now establish a database connection
...

Provided you have established appropriate read permissions in credsdir
the secrets are protected. Because they never appear in your code they
stay out of the repository so that many years hence they cannot be
discovered under any nefarious circumstances.
"""
import os


def getcreds(fname, project, credsroot='/var/www/creds', credsdir=None):
    """ return a list of userid and password and perhaps other data """
    if credsdir is None:
        credsdir = os.path.join(credsroot, project)
    creds = list()
    fname = os.path.join(credsdir, fname).replace("\\", "/")
    with open(fname, 'r') as f:
        for line in f:
            # remove leading/trailing whitespace and append to list
            creds.append(line.strip())
    if not creds:
        raise ValueError('The list of credentials is empty')
    return creds

