#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logger import get_logger

log = get_logger(__name__)


def test_log():
    log.debug('Debug message')
    log.info('Info message')
    log.warning('Warning message')
    log.error('Error message')
    log.critical('Critical message')
