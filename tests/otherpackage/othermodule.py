#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)


def test_log():
    log.debug('Other module debug message')
    log.info('Other module info message')
    log.warning('Other module warning message')
    log.error('Other module error message')
    log.critical('Other module critical message')
