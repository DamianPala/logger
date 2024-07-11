# logger

-----

Python logger with some advanced features.

**Table of Contents**

- [Installation](#installation)
- [Features](#features)
- [Development Environment](#development-environment)
- [Testing](#testing)
- [License](#license)

## Installation

```shell
$ pip install git+https://github.com/DamianPala/logger.git
```

## Features

### Log like a print

```shell
>>> log.info('This is a message', 'with', 'args', 1, 2.0)
This is a message with args 1 2.0
```

### Log with keyword arguments

```shell
>>> log.info('This is a message', 'with', 'kwargs', kw1=1, kw2=2.0)
This is a message with kwargs kw1=1 kw2=2.0
```

### Set log level from sys argv

Logger checks arguments with you run your code. 
In case of using `-v` or `--verbose` it will set the log level to `DEBUG` automatically.

### Colored log level

Log level keyword is coloured to improved visibility.

### Easy file logging

Use `enable_file_logging` method to enable logging to the file. You can set the desired log level and format as well. 
Log messages will be cleared from ANSI escape sequences.

### Caplog integration

Logger easily integrates with `caplog`. You need to put following code into your `conftest.py` file:

```python
import pytest
from _pytest.logging import LogCaptureFixture
from logger import logger


@pytest.fixture
def caplog(caplog: LogCaptureFixture) -> LogCaptureFixture:
    logger.caplog_integrate(caplog.handler)
    yield caplog
```

## Development Environment

1. Install min Python 3.8
2. Install `hatchling` globally:

   ```shell
   $ python -m pip install hatch
   ```
   
   or

   ```shell
   $ pipx install hatch
   ```

3. Open root package directory, create a virtual environment, install dependencies and enter the shell (OPTIONAL).  

   ```shell
   $ hatch shell
   ```

## Testing

For testing, `hatchling` will create virtual environment automatically.  
To run a test you can use the command like this:

```shell
$ hatch test -- -s tests/test_main.py::TestMsgFormat::test_simple_msg
```

or

```shell
$ hatch test
```

To run all tests.

> **WARNING!** There is a bug in hatchling 1.12.0 affecting testing. In case of test is not finding sources execute one time:
> `hatch test -py X.X` where `X.X` is your python version. 

## License

`logger` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
