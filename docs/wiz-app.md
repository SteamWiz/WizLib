# WizApp

The `WizApp` class is the root of all WizLib-based CLI applications. It serves as the entry point and orchestrator for your command-line application.

## Overview

Applications that use the WizLib framework inherit from WizApp and define required attributes to configure the application behavior. The WizApp class handles argument parsing, command execution, and error handling.

## Required Attributes

When creating a class that inherits from WizApp, you need to define these attributes:

| Attribute | Description |
|-----------|-------------|
| `name` | Name of the application, used in argparse and configuration |
| `base` | Base command class, typically defined in command/__init__.py |
| `handlers` | List of Handler classes used by this app |

## Available Methods

WizApp provides the following methods that you can use without overriding:

| Method | Description |
|--------|-------------|
| `main()` | Class method to call from a `__main__` entrypoint |
| `start(*args, debug=False)` | Class method to call from a Python entrypoint |
| `run(**vals)` | Perform a command with the specified values |
| `parse_run(*args)` | For testing, parse just the command part and run |

**Note:** Typically, you don't need to override these methods. They provide the core functionality of the WizApp framework.

## Basic Usage

Here's a simple example of how to define a WizApp application:

```python
# __init__.py
from wizlib.app import WizApp
from wizlib.config_handler import ConfigHandler
from wizlib.stream_handler import StreamHandler
from wizlib.ui_handler import UIHandler
from myapp.command import MyAppCommand

class MyApp(WizApp):
    name = 'myapp'
    base = MyAppCommand
    handlers = [ConfigHandler, StreamHandler, UIHandler]
```

```python
# __main__.py
from myapp import MyApp

if __name__ == '__main__':
    MyApp.main()
```

## Error Handling

WizApp provides built-in error handling through the following mechanisms:

- `AppCancellation`: A special exception that can be raised to cancel the application with an optional message
- Debug mode: When debug=True is passed to start(), exceptions are re-raised for debugging
- Standard error output: When debug=False, errors are printed to stderr with appropriate formatting
