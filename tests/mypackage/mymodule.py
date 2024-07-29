#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logger import get_logger

log = get_logger(__name__)


def test_log():
    log.debug('My module debug message')
    log.info('My module info message')
    log.warning('My module warning message')
    log.error('My module error message')
    log.critical('My module critical message')
