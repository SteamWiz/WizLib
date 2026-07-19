# StreamHandler

The `StreamHandler` simplifies handling of input data for WizLib applications, particularly for non-interactive (non-tty) inputs such as pipes or redirected files.

## Overview

The StreamHandler provides a consistent way to access input data, whether it comes from:

- Standard input (stdin) via a pipe
- A file specified with the `--stream` option
- Any other source that might be added in the future

Despite its name, the StreamHandler doesn't actually process data as a stream. Instead, it reads all input data at once when the command starts, making it available to commands as a single text value.

## How It Works

When a WizLib application is initialized with StreamHandler in its `handlers` list, the handler:

1. Checks if input is being provided via stdin (e.g., through a pipe)
2. Checks if a file path was provided via the `--stream` option
3. Reads all the input data at once
4. Makes the data available to commands via `self.app.stream.text`

## Accessing Stream Data

Commands can access the input data using:

```python
# In a command's execute() or handle_vals() method
input_data = self.app.stream.text
```

## Command-Line Usage

Users can provide input to a WizLib application in several ways:

```bash
# Using a pipe
echo "Hello, World!" | myapp process

# Using input redirection
myapp process < input.txt

# Using the --stream option
myapp process --stream input.txt
```

## Example Usage in a Command

Here's how you might use the StreamHandler in a command:

```python
from myapp.command import MyAppCommand

class ProcessCommand(MyAppCommand):
    name = 'process'
    
    @MyAppCommand.wrap
    def execute(self):
        # Get the input data
        data = self.app.stream.text
        
        if not data:
            return "No input data provided"
        
        # Process the data
        lines = data.strip().split('\n')
        line_count = len(lines)
        
        self.status = f"Processed {line_count} lines"
        return f"Input contained {line_count} lines"
```

## Adding StreamHandler to Your Application

To enable the StreamHandler in your WizLib application, include it in the `handlers` list:

```python
from wizlib.app import WizApp
from wizlib.stream_handler import StreamHandler
from myapp.command import MyAppCommand

class MyApp(WizApp):
    name = 'myapp'
    base = MyAppCommand
    handlers = [StreamHandler]  # Include StreamHandler
```

## Testing with StreamHandler

For testing commands that use StreamHandler, you can create a fake StreamHandler with predefined content:

```python
from wizlib.stream_handler import StreamHandler

# Create a command with a fake stream handler
command = MyCommand()
command.app = MyApp()
command.app.stream = StreamHandler.fake("Test input data")

# Now command.execute() will use the fake stream data
result = command.execute()
```
