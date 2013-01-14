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
        with open('README.md') as f:
            return f.read().strip()
    except IOError:
        return ''


setup(
    name='prettyexc',
    version=get_version(),
    description='Easy pretty-look exception interface.',
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
        'distribute',
    ],
)
