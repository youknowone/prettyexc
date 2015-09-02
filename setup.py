from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    with open('prettyexc/version.txt') as f:
        return f.read().strip()


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''


setup(
    name='prettyexc',
    version=get_version(),
    description='Make any exception human readable in easy way.',
    long_description=get_readme(),
    author='Jeong YunWon',
    author_email='jeong+prettyexc@youknowone.org',
    url='https://github.com/youknowone/prettyexc',
    packages=(
        'prettyexc',
    ),
    package_data={
        'prettyexc': ['version.txt']
    },
    install_requires=[
        'six',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
     ],
)
