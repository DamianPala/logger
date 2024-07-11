import pytest
from _pytest.logging import LogCaptureFixture
from logger import logger


@pytest.fixture
def caplog(caplog: LogCaptureFixture) -> LogCaptureFixture:
    logger.caplog_integrate(caplog.handler)
    yield caplog
