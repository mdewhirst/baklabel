from distutils.core import setup
from filemov import filemov

files = ['doc/*.txt', 'test/*.py']

setup(
        name='filemov',
        version = '1.1.1-2728-py2.7',
        description='File relocation according to defined strategy',
        author='Mike Dewhirst',
        author_email='miked dewhirst com au',
        url='http://svn.pczen.com.au/repos/gpl3/filemov/distrib',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: System :: Archiving :: Backup',
            'Topic :: Utilities',
            ],
        scripts=[],
        long_description="""%s""" % filemov.longdesc,
        packages=['filemov'],
        package_data={'filemov': files},

)
