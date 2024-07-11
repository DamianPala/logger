#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import pytest
import tempfile
import subprocess
from inspect import currentframe
from pathlib import Path

import src.logger as logger


@pytest.fixture
def log() -> logger.Logger:
    _log = logger.get_logger('mylogger')
    _log.setLevel(logger.DEFAULT_LOG_LEVEL)
    return _log


class TestMsgFormat:
    def test_simple_msg(self, log, caplog):
        log.info('This is a message')
        assert re.search(rf'\[.*\] - mylogger:{currentframe().f_lineno - 1} \[INFO\]: This is a message', caplog.text)

    def test_msg_with_args(self, log, caplog):
        log.info('This is a message', 'with', 'args', 1, 2.0)
        assert re.search(rf'\[.*\] - mylogger:{currentframe().f_lineno - 1} \[INFO\]: This is a message with args 1 2.0', caplog.text)

    def test_msg_with_kwargs(self, log, caplog):
        log.info('This is a message', 'with', 'kwargs', kw1=1, kw2=2.0)
        assert re.search(rf'\[.*\] - mylogger:{currentframe().f_lineno - 1} \[INFO\]: This is a message with kwargs kw1=1 kw2=2.0', caplog.text)


class TestLevels:
    def test_all_levels(self, log, caplog):
        log.setLevel(logger.NOTSET)
        log.debug('Debug message')
        assert re.search(rf'\[.*\] - mylogger:{currentframe().f_lineno - 1} \[DEBUG\]: Debug message', caplog.text)
        log.info('Info message')
        assert re.search(rf'\[.*\] - mylogger:{currentframe().f_lineno - 1} \[INFO\]: Info message', caplog.text)
        log.warning('Warning message')
        assert re.search(rf'\[.*\] - mylogger:{currentframe().f_lineno - 1} \[WARNING\]: Warning message', caplog.text)
        log.error('Error message')
        assert re.search(rf'\[.*\] - mylogger:{currentframe().f_lineno - 1} \[ERROR\]: Error message', caplog.text)
        log.critical('Critical message')
        assert re.search(rf'\[.*\] - mylogger:{currentframe().f_lineno - 1} \[CRITICAL\]: Critical message', caplog.text)

    def test_level_debug(self, log, caplog):
        log.setLevel(logger.DEBUG)
        log.debug('Debug message')
        assert 'Debug message' in caplog.text
        log.info('Info message')
        assert 'Info message' in caplog.text
        log.warning('Warning message')
        assert 'Warning message' in caplog.text
        log.error('Error message')
        assert 'Error message' in caplog.text
        log.critical('Critical message')
        assert 'Critical message' in caplog.text

    def test_level_info(self, log, caplog):
        log.setLevel(logger.INFO)
        log.debug('Debug message')
        assert 'Debug message' not in caplog.text
        log.info('Info message')
        assert 'Info message' in caplog.text
        log.warning('Warning message')
        assert 'Warning message' in caplog.text
        log.error('Error message')
        assert 'Error message' in caplog.text
        log.critical('Critical message')
        assert 'Critical message' in caplog.text

    def test_level_warning(self, log, caplog):
        log.setLevel(logger.WARNING)
        log.debug('Debug message')
        assert 'Debug message' not in caplog.text
        log.info('Info message')
        assert 'Info message' not in caplog.text
        log.warning('Warning message')
        assert 'Warning message' in caplog.text
        log.error('Error message')
        assert 'Error message' in caplog.text
        log.critical('Critical message')
        assert 'Critical message' in caplog.text

    def test_level_error(self, log, caplog):
        log.setLevel(logger.ERROR)
        log.debug('Debug message')
        assert 'Debug message' not in caplog.text
        log.info('Info message')
        assert 'Info message' not in caplog.text
        log.warning('Warning message')
        assert 'Warning message' not in caplog.text
        log.error('Error message')
        assert 'Error message' in caplog.text
        log.critical('Critical message')
        assert 'Critical message' in caplog.text

    def test_level_critical(self, log, caplog):
        log.setLevel(logger.CRITICAL)
        log.debug('Debug message')
        assert 'Debug message' not in caplog.text
        log.info('Info message')
        assert 'Info message' not in caplog.text
        log.warning('Warning message')
        assert 'Warning message' not in caplog.text
        log.error('Error message')
        assert 'Error message' not in caplog.text
        log.critical('Critical message')
        assert 'Critical message' in caplog.text

    def test_set_global_level(self, log, caplog):
        log.setLevel(logger.DEBUG)
        logger.set_level(logger.ERROR)
        log.debug('Debug message')
        assert 'Debug message' not in caplog.text
        log.info('Info message')
        assert 'Info message' not in caplog.text
        log.warning('Warning message')
        assert 'Warning message' not in caplog.text
        log.error('Error message')
        assert 'Error message' in caplog.text
        log.critical('Critical message')
        assert 'Critical message' in caplog.text

    def test_set_level_from_sys_argv(self):
        output = subprocess.run([sys.executable, '-m', 'mypackage'],
                                cwd=Path(__file__).parent,
                                capture_output=True,
                                text=True).stdout
        assert 'Debug message' not in output
        assert 'Info message' in output
        assert 'Warning message' in output
        assert 'Error message' in output
        assert 'Critical message' in output

        output = subprocess.run([sys.executable, '-m', 'mypackage', '-v'],
                                cwd=Path(__file__).parent,
                                capture_output=True,
                                text=True).stdout
        assert 'Debug message' in output
        assert 'Info message' in output
        assert 'Warning message' in output
        assert 'Error message' in output
        assert 'Critical message' in output


def test_file_logging(log):
    log.setLevel(logger.INFO)
    log_file = tempfile.NamedTemporaryFile(delete=False).name
    log.enable_file_logging(log_file)
    log.debug('Debug message')
    log.info('Info message')
    log.warning('Warning message')
    log.error('Error message')
    log.critical('Critical message')
    log_file_text = Path(log_file).read_text()
    assert '[INFO]: Info message' in log_file_text
    assert '[WARNING]: Warning message' in log_file_text
    assert '[ERROR]: Error message' in log_file_text
    assert '[CRITICAL]: Critical message' in log_file_text


def test_valid_package_name_when_run_as_a_package():
    output = subprocess.run([sys.executable, '-m', 'mypackage'],
                            cwd=Path(__file__).parent,
                            capture_output=True,
                            text=True).stdout
    assert re.search(r'\[.*\] - mypackage\.mymodule:\d+ \[INFO\]: Info message', output)
