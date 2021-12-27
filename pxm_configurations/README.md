# PXM Configurations

## Introduction

This folder contains all `.conf` files related to different configurations as needed by the project for its continuous
usage.

All the configurations need to be mentioned in its suitable configuration files, and they will be automatically loaded
as environment variables before the server starts execution, with the key as the config key and value same as the config
value. hence, to access any of these configurations you are needed to call the relevant method to retrieve environment
variable from the system.

For Example,

For a config file, let's say `example.conf`:

```
    # The configuration should be in key value manner
    example.url = www.example.org
```

To access this configuration using `python`:

```python
import os

URL = os.getenv('example.url')
print('Your url is', URL)

# Output:
# www.example.org
```
