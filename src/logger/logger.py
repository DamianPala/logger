#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import logging
from typing import IO, Optional, List
from pathlib import Path
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from colorama import Fore, Style, just_fix_windows_console

just_fix_windows_console()

DEFAULT_LOG_LEVEL = INFO
DEFAULT_LOG_FORMAT = '[%(asctime)s] - %(name)s:%(lineno)d [%(levelname)s]: %(message)s'
_PACKAGE_NAME = (Path(__file__) / '..').resolve().name

LOG_COLORS = {
    DEBUG: Fore.MAGENTA,
    INFO: Fore.GREEN,
    WARNING: Fore.YELLOW,
    ERROR: Fore.RED,
    CRITICAL: Fore.RED + Style.BRIGHT
}


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt: Optional[str] = None) -> None:
        fmt = fmt or DEFAULT_LOG_FORMAT
        super().__init__(fmt=fmt)

    def format(self, record: logging.LogRecord) -> str:
        if _isatty(sys.stdout) and _isatty(sys.stderr):
            # Only color log messages when sys.stdout and sys.stderr are sent to the terminal.
            log_color = LOG_COLORS.get(record.levelno, '')
            record.levelname = f'{log_color}{record.levelname}{Style.RESET_ALL}'
        return super().format(record)


class ColorCleanFormatter(logging.Formatter):
    def __init__(self, fmt: Optional[str] = None) -> None:
        fmt = fmt or DEFAULT_LOG_FORMAT
        self._ansi_escape = re.compile(r'\x1B\[[0-9;]*m')
        super().__init__(fmt=fmt)

    def format(self, record: logging.LogRecord) -> str:
        record.msg = self._clear_ansi(str(record.msg))
        record.levelname = self._clear_ansi(record.levelname)
        return super().format(record)

    def _clear_ansi(self, text: str) -> str:
        return self._ansi_escape.sub('', text)


class Logger(logging.Logger):
    loggers: List['Logger'] = []

    def __init__(self,
                 name: str,
                 level: int = NOTSET,
                 fmt: Optional[str] = None,
                 propagate: bool = False) -> None:
        root_level = logging.root.getEffectiveLevel()
        if level == NOTSET:
            level = root_level if root_level < DEFAULT_LOG_LEVEL else DEFAULT_LOG_LEVEL
        level = self._load_level_from_sys_argv(level)
        super().__init__(name, level)
        fmt = fmt or DEFAULT_LOG_FORMAT
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(ColorFormatter(fmt))
        del self.handlers[:]
        self.addHandler(ch)
        self.propagate = propagate
        self.loggers.append(self)
        self.caplog_handler: Optional[logging.Handler] = None

    def setLevel(self, level: int) -> None:
        super().setLevel(level)
        for handler in self.handlers:
            if handler is not logger.caplog_handler:
                handler.setLevel(level)

    def enable_file_logging(self, filename: str, level: Optional[int] = None, fmt: Optional[str] = None) -> None:
        fh = logging.FileHandler(filename)
        fh.setLevel(level or self.level)
        formatter = ColorCleanFormatter(fmt or DEFAULT_LOG_FORMAT)
        fh.setFormatter(formatter)
        self.addHandler(fh)

    def caplog_integrate(self, caplog_handler) -> None:
        self.caplog_handler = caplog_handler
        self.addHandler(caplog_handler)
        for _logger in self.loggers:
            _logger.addHandler(caplog_handler)

    def debug(self, msg, *args, **kwargs) -> None:
        self._log_message(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs) -> None:
        self._log_message(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs) -> None:
        self._log_message(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs) -> None:
        self._log_message(logging.ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs) -> None:
        self._log_message(logging.ERROR, msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs) -> None:
        self._log_message(logging.CRITICAL, msg, *args, **kwargs)

    def _log_message(self, level, msg, *args, **kwargs) -> None:
        filtered_kwargs = {k: v for k, v in kwargs.items()
                           if k not in {'exc_info', 'stack_info', 'stacklevel', 'extra'}}
        if args:
            message = msg % args if '%' in msg else ' '.join((msg, *map(str, args)))
        else:
            message = msg
        if filtered_kwargs:
            message += ' ' + ' '.join(f'{key}={value}' for key, value in filtered_kwargs.items())
        super().log(level, message, **{k: v for k, v in kwargs.items()
                                       if k in {'exc_info', 'stack_info', 'stacklevel', 'extra'}})

    def findCaller(self, stack_info=False, stacklevel=1):
        return super().findCaller(stacklevel=4)

    @staticmethod
    def _load_level_from_sys_argv(level: int) -> int:
        for i in range(len(sys.argv)):
            if sys.argv[i] == '-v' or sys.argv[i] == '--verbose':
                return DEBUG
        else:
            return level


def get_logger(name: str) -> Logger:
    """
    Get a logger with the given ``name``.
    """
    _logger = Logger(name)
    _logger.setLevel(logger.level)
    for handler in _logger.handlers:
        handler.setLevel(logger.level)
    return _logger


def set_level(level: int) -> None:
    """
    Change the global logger log-level in all packages and modules using Logger.
    """
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
    for _logger in Logger.loggers:
        _logger.setLevel(level)
        for handler in _logger.handlers:
            handler.setLevel(level)


def enable_file_logging(filename: str, level: Optional[int] = None, fmt: Optional[str] = None) -> None:
    fh = logging.FileHandler(filename)
    formatter = ColorCleanFormatter(fmt or DEFAULT_LOG_FORMAT)
    fh.setFormatter(formatter)
    fh.setLevel(level or logging.root.level)
    logging.root.addHandler(fh)

    for _logger in Logger.loggers:
        fh = logging.FileHandler(filename)
        formatter = ColorCleanFormatter(fmt or DEFAULT_LOG_FORMAT)
        fh.setFormatter(formatter)
        fh.setLevel(level or _logger.level)
        _logger.addHandler(fh)


def _isatty(stream: IO) -> bool:
    """
    Returns ``True`` if the stream is part of a tty.
    Borrowed from ``click._compat``.
    """
    try:
        return stream.isatty()
    except Exception:  # noqa
        return False


logger = Logger(_PACKAGE_NAME)
