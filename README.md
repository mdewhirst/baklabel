
Baklabel is intended for use in automated scripts to deliver a sensible directory path
fragment (or label) each day to construct a grandfathered local backup.

Import baklabel.Grandad to produce today's label fragment.

See test_baklabel.py for examples of how to call Grandad

It is also a stand-alone utility to find the backup label produced for any given date
and set of options.

python3 baklabel.py -h  to see command line usage and options.

Python 3.x (Python 2.7 should also work but is no longer tested)

In the doc directory of the baklabel repo, see release_note.txt for more detail on the
package, examples.txt for baklabel output examples and backup_howto.txt for a sample
backup script for Windows.


Properly grandfathered, there needs to be a daily backup to one of 23 separate tapes,
sets of media or local directories on a storage device. This complement is made up of
6 weekday backups, 5 week-end backups, 11 month-end backups plus one for year-end.

23 backups is quite economical for 12 months coverage.

This represents real comfort when retrieving data which has been compromised at some
unknown point in the past.


Source:  https://github.com/mdewhirst/baklabel

Mike Dewhirst
miked@dewhirst.com.au

