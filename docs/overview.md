
# WizLib

⚠️ DISCLAIMER: This is a hobby/personal project. Not a commercial product. Not for production use.

## Build configurable CLI tools easily in Python (a framework)

A Python framework that simplifies the creation of command-line interface (CLI) applications. It provides a structured approach to building CLI tools with a focus on modularity, testability, and developer experience.

## Framework Capabilities

- **Easy addition of loosely coupled subcommands**: Add new commands by simply creating new files in the `command` directory
- **Normalized access to configuration files**: Access configuration from environment variables or YAML files with a consistent API
- **Standardized use of stdin, stdout, and stderr**: Simplified I/O handling across your application following Unix-style norms
- **Plugin-type system for handling alternate UIs**: Support for different user interfaces with a vision of supporting shell, repl, terminal, web, Slack, and MCP server interfaces
- **Simple line editor with completion support**: Enhanced user input experience
- **Abstracts some of the argparse complexity**: Simplified command-line argument parsing
- **Applies conventions to application code structure**: Consistent organization of your application
- **Supports test-driven development and CI/CD**: Built with testing in mind

## Important Documentation Notes

- **When developing tests**: Always consult the [Test helpers](testing.md) documentation for proper mocking and testing of WizLib components
- **When working with configuration**: Refer to the [ConfigHandler](config-handler.md) documentation for details on how to access and manage configuration values
- **When implementing commands**: Review the [Command](command.md) documentation for best practices and required methods


## Approach

WizLib wraps the built-in ArgumentParser with a set of functions, classes, and conventions.

Commands exist independently. To add a new command, simply add a Python file in the `command` directory with a class definition that inherits from the base command. The command will automatically appear as an option in usage, and the implementation has access to handlers for arguments, inputs, user interfaces, and values from a configuration file for the application.

### Application Structure

A WizLib application has the following directory structure at a minimum. In this case, the app is called `Sample` with the main command `sample` and one subcommand `doit`.

```
sample
 ├─ .git
 └─ sample
     ├─ __init__.py
     ├─ __main__.py
     └─ command
         ├─ __init__.py
         └─ doit_command.py
```

### Quick Start Example

1. Define your app in `__init__.py`:

```python
from wizlib.app import WizApp
from sample.command import SampleCommand

class Sample(WizApp):
    name = 'sample'
    base = SampleCommand
```

2. Create an entry point in `__main__.py`:

```python
from sample import Sample

if __name__ == '__main__':
    Sample.main()
```

3. Define your base command in `command/__init__.py`:

```python
from wizlib.command import WizCommand

class SampleCommand(WizCommand):
    default = 'doit'
```

4. Create a command in `command/doit_command.py`:

```python
from sample.command import SampleCommand

class DoitCommand(SampleCommand):
    name = 'doit'
    
    @classmethod
    def add_args(cls, parser):
        parser.add_argument('task', nargs='?', default='something')
    
    def execute(self):
        return f"Doing {self.task}!"
```

5. Run your app:

```bash
python -m sample doit "something important"
```

Output:
```
Doing something important!
```

## Core Components

WizLib defines several Python classes and functions for inclusion in projects:

- [WizApp](./wiz-app.md) - Base class for a WizLib app
- [Command](./command.md) - Root class for the app-specific command class, which forms the base class for other commands
- [ConfigHandler](./config-handler.md) - Handles configuration, either through environment variables or a YAML configuration file
- [StreamHandler](./stream-handler.md) - Simplifies handling of input via stdin for non-tty inputs such as pipes
- [ClassFamily](./class-family.md) - A primitive class that loads all subclasses in a directory into a "family" which can be queried for lookup
- [SuperWrapper](./super-wrapper.md) - A primitive class that "wraps" subclass methods, so that the superclass method gets called before and after the subclass method
- [UIHandler](./ui-handler.md) - Handles user interface interactions

## How Components Work Together

1. **WizApp** initializes the application and sets up the command structure
2. **Command** classes define the available commands and their behavior
3. **Handlers** (ConfigHandler, StreamHandler, UIHandler) provide services to commands
4. **ClassFamily** automatically discovers and registers command classes
5. **SuperWrapper** manages method inheritance and execution order

## Documentation

Documentation is built with [mdBook](https://rust-lang.github.io/mdBook/) and deployed automatically to [wizlib.steamwiz.io](https://wizlib.steamwiz.io) on every push to `main`.
