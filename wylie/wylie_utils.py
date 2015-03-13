#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

config_file = '~/.wylie_config.py'
sys.path.append(os.path.dirname(os.path.expanduser(config_file)))
	
from wylie_config import settings

__title__ = 'wylie'
__version__ = '0.1'
__author__ = '@c0ding'
__repo__ = 'https://github.com/c0ding/wylie'
__license__ = 'Apache v2.0 License'
