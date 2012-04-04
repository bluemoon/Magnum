#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys



from setuptools import setup, find_packages



if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name='magnum',
    version='0.1',
    description='Python ORM for Humans.',
    author='Bradford Toney',
    author_email='bradford.toney@gmail.com',
    packages=packages=['magnum'],
    include_package_data=True,
)