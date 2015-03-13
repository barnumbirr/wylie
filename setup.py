#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'wylie',
    version = '0.1',
    url = 'https://github.com/c0ding/wylie',
    download_url = 'https://github.com/c0ding/wylie/archive/master.zip',
    author = 'c0ding',
    author_email = 'me@martinsimon.me',
    license = 'Apache v2.0 License',
    packages = ['wylie'],
    description = 'Get Jenkins build notifications on OSX.',
    long_description = file('README.md','r').read(),
    keywords = ['Jenkins', 'continuous integration', 'notification', 'git', 'mercurial', 'svn', 'OSX'],
)
