# Command

In WizLib, "commands" are actually subcommands in the shell sense. A WizLib-based application is a shell command (e.g., `myapp`), and the "commands" within it are subcommands (e.g., `myapp create ...`). These subcommands define the various actions your application can perform.

## Command Organization

Commands live in the `command/` directory and inherit from a single base command, which itself inherits from `WizCommand`. This structure allows WizLib to automatically discover and register all commands in your application.

The base command class is typically defined in `command/__init__.py`, and individual command classes are defined in separate files within the `command` directory, following the naming pattern `<command_name>_command.py`.

## Command Implementation

When implementing a command, you need to:

1. Define a `name` attribute that users will type to invoke the command
2. Override specific methods to define the command's behavior

The three key methods to override are:

1. `add_args` - Define command-line arguments
2. `handle_vals` - Process and validate argument values
3. `execute` - Perform the command's action

### The `add_args` Method

This class method defines the command-line arguments that your command accepts.

**Method Signature:**
```python
@classmethod
def add_args(cls, parser: WizParser):
    # Add arguments here
```

**Example:**
```python
@classmethod
def add_args(cls, parser: WizParser):
    parser.add_argument('filename', help='File to process')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
```

This method uses the standard `argparse` library syntax for defining arguments. The parser is an instance of `WizParser`, which extends `ArgumentParser`.

### The `handle_vals` Method

This method processes and validates the argument values. It's also where you can prompt for missing values or set default values.

**Method Signature:**
```python
def handle_vals(self):
    super().handle_vals()
    # Process values here
```

**Example:**
```python
def handle_vals(self):
    super().handle_vals()  # Always call the superclass method first
    
    # Check if a required argument was provided, prompt if not
    if not self.provided('filename'):
        self.filename = self.app.ui.get_input('Enter filename: ')
    
    # Set a default value for an optional argument
    if not hasattr(self, 'format'):
        self.format = 'json'
```

**Important:** Always call `super().handle_vals()` at the beginning of your implementation to ensure proper inheritance.

The `provided()` method (which you should not override) helps you check if an argument was provided by the user. It handles various edge cases, such as boolean flags that might be `False`.

### The `execute` Method

This method performs the actual command action and returns a result string.

**Method Signature:**
```python
@BaseCommand.wrap
def execute(self):
    # Perform the command action
    return "Result string"
```

**Example:**
```python
@MyAppCommand.wrap
def execute(self):
    # Process the file
    result = process_file(self.filename, verbose=self.verbose)
    
    # Set a status message (printed to stderr)
    self.status = f"Processed {self.filename} successfully"
    
    # Return the result (printed to stdout)
    return result
```

**Important:** 
1. Use the `@BaseCommand.wrap` decorator (replacing `BaseCommand` with your actual base command class name) to ensure proper method wrapping.
2. The string returned by `execute()` is printed to stdout.
3. Setting `self.status` will print a message to stderr, following the Unix convention of separating normal output from status messages.

## Command Cancellation

If a command needs to be cancelled, it can raise a `CommandCancellation` exception:

```python
from wizlib.command import CommandCancellation

def handle_vals(self):
    super().handle_vals()
    if not self.provided('filename'):
        raise CommandCancellation("No filename provided")
```

## Complete Example

Here's a complete example of a command implementation:

```python
from wizlib.parser import WizParser
from wizlib.command import CommandCancellation
from myapp.command import MyAppCommand

class ProcessCommand(MyAppCommand):
    """Process a file with various options"""

    name = 'process'

    @classmethod
    def add_args(cls, parser: WizParser):
        parser.add_argument('filename', nargs='?', help='File to process')
        parser.add_argument('--format', '-f', choices=['json', 'xml', 'yaml'], 
                           default='json', help='Output format')
        parser.add_argument('--verbose', '-v', action='store_true', 
                           help='Enable verbose output')

    def handle_vals(self):
        super().handle_vals()
        
        # Check if filename was provided, prompt if not
        if not self.provided('filename'):
            self.filename = self.app.ui.get_input('Enter filename: ')
            
            # Validate the filename
            if not os.path.exists(self.filename):
                raise CommandCancellation(f"File not found: {self.filename}")

    @MyAppCommand.wrap
    def execute(self):
        # Process the file based on the format
        if self.verbose:
            print(f"Processing {self.filename} in {self.format} format...", 
                  file=sys.stderr)
            
        result = process_file(self.filename, format=self.format)
        
        self.status = f"Processed {self.filename} successfully"
        return result
```
