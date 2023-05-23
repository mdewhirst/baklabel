from distutils.core import setup
from shorts import shorts as module

files = ['doc/*.txt', 'test/*.py']
srcdir = progname = 'shorts'
setup(
        name=progname,
        version = '0.1.1-2725',
        description='Re-write group_login.bat for Project Shorts',
        author='Mike Dewhirst',
        author_email='miked dewhirst com au',
        url='http://svn.pczen.com.au/repos/gpl3/shorts/distrib',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Topic :: Utilities',
            ],
        scripts=[],
        long_description="""%s""" % module.longdesc,
        packages=[progname],
        package_data={srcdir: files},

)
