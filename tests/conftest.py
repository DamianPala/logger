import pytest
from _pytest.logging import LogCaptureFixture
from src.logger import logger


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    logger.caplog_integrate(caplog.handler)
    yield caplog
