# Testing

WizLib provides several utilities to simplify testing of WizLib applications, making it easier to write comprehensive unit tests for your commands and application logic.

> **⚠️ IMPORTANT: When testing WizLib applications, always use the provided testing utilities and fake handlers described in this document. Do not attempt to mock WizLib components manually, as this can lead to subtle bugs and test failures.**

## Overview

Testing WizLib applications can be challenging because they often:

1. Interact with users through the UI
2. Read from standard input streams
3. Write to standard output and error streams
4. Access configuration values
5. Parse command-line arguments

WizLib's testing utilities help you mock these interactions and focus on testing your application logic.

## WizLibTestCase

The `WizLibTestCase` class is a subclass of `unittest.TestCase` that provides convenience methods for patching inputs and outputs in WizLib applications.

### Key Methods

| Method | Description |
|--------|-------------|
| `patch_stream(val: str)` | Patch stream input such as pipes for StreamHandler |
| `patch_ttyin(val: str)` | Patch input typed by a user in shell UI |
| `patcherr()` | Capture output from standard error |
| `patchout()` | Capture output from standard output |

### Example Usage

```python
from wizlib.test_case import WizLibTestCase
from myapp import MyApp

class MyAppTest(WizLibTestCase):
    
    def test_input_handling(self):
        # Simulate user input 'laughter' and capture stdout
        with self.patch_stream('laughter'), self.patchout() as output:
            # Run the application
            MyApp.start('dance')
            
            # Check the output
            output.seek(0)
            self.assertIn('Dancing laughter', output.read())
    
    def test_user_interaction(self):
        # Simulate user typing 'y' when prompted and capture stderr
        with self.patch_ttyin('y'), self.patcherr() as error:
            MyApp.start('delete', 'file.txt')
            
            # Check the error output
            error.seek(0)
            self.assertIn('File deleted', error.read())
```

These methods can be combined as needed to simulate complex interactions. You can also use them with Python's standard `unittest.mock` library for more advanced patching.

## Fake Handlers

WizLib provides "fake" versions of its handlers for testing purposes. These allow you to simulate specific behaviors without setting up the real handlers.

### ConfigHandler.fake

Creates a fake configuration handler with predefined values:

```python
from wizlib.config_handler import ConfigHandler
from myapp import MyApp
from myapp.command import ProcessCommand

def test_config_dependent_command(self):
    # Create an app with a fake config
    app = MyApp()
    app.config = ConfigHandler.fake(
        myapp_api_url='https://test-api.example.com',
        myapp_timeout='30'
    )
    
    # Create and run a command that uses config values
    command = ProcessCommand(app)
    result = command.execute()
    
    # Verify the result
    self.assertEqual('Processed data from https://test-api.example.com', result)
```

> **⚠️ CRITICAL: Never directly assign a dictionary to `app.config` in tests (e.g., `app.config = {'myapp-api-url': 'value'}`). This will bypass the ConfigHandler's functionality and can cause tests to use real configuration values instead of test values. Always use `ConfigHandler.fake()` as shown above.**

**Note**: When creating fake config values, use underscores in the parameter names, but the values will be accessed with hyphens in your code:

```python
# In test:
app.config = ConfigHandler.fake(myapp_api_url='https://example.com')

# In application code:
url = self.app.config.get('myapp-api-url')
```

### StreamHandler.fake

Creates a fake stream handler with predefined input:

```python
from wizlib.stream_handler import StreamHandler
from myapp import MyApp
from myapp.command import ParseCommand

def test_stream_processing(self):
    # Create an app with fake stream input
    app = MyApp()
    app.stream = StreamHandler.fake('{"name": "Test", "value": 42}')
    
    # Create and run a command that processes stream input
    command = ParseCommand(app)
    result = command.execute()
    
    # Verify the result
    self.assertEqual('Parsed: Test (42)', result)
```

## Testing Commands

Since commands are the core of WizLib applications, WizLib provides specific utilities for testing them.

### Direct Command Testing

To test a command's execution logic without going through argument parsing:

```python
def test_command_execution(self):
    # Create an app
    app = MyApp()
    
    # Create a command with specific arguments
    command = CalculateCommand(app, value=10, operation='square')
    
    # Execute the command
    result = command.execute()
    
    # Verify the result
    self.assertEqual(100, result)
```

### Testing Command Parsing and Execution

To test both argument parsing and command execution:

```python
def test_command_parsing_and_execution(self):
    # Capture stdout
    with self.patchout() as output:
        # Create an app and run a command with arguments
        app = MyApp()
        app.parse_run('calculate', '--value', '10', '--operation', 'square')
        
        # Check the output
        output.seek(0)
        self.assertIn('Result: 100', output.read())
```

The `parse_run` method is a shortcut that parses the arguments and runs the command without going through the full application startup process.

## Testing UI Interactions

For testing UI interactions, you can use a combination of the patching methods and Python's mock library:

```python
from unittest.mock import patch
from wizlib.ui import Chooser, Choice

def test_ui_interaction(self):
    # Create a chooser that the command will use
    chooser = Chooser("Select operation", "add", [
        Choice("add", "a"),
        Choice("subtract", "s"),
        Choice("multiply", "m")
    ])
    
    # Patch the UI's get_option method to return a specific choice
    with patch('myapp.ui.MyAppUI.get_option', return_value="multiply"):
        # Create an app
        app = MyApp()
        
        # Create and run a command that uses UI
        command = InteractiveCalculateCommand(app, value1=5, value2=4)
        result = command.execute()
        
        # Verify the result
        self.assertEqual(20, result)  # 5 * 4 = 20
```

## Best Practices for Testing WizLib Applications

1. **Use WizLibTestCase**: Inherit from WizLibTestCase to get access to the patching methods
2. **Test Commands Individually**: Test each command's functionality in isolation
3. **Test Command Parsing**: Test that arguments are correctly parsed and passed to commands
4. **Mock External Dependencies**: Use Python's mock library to mock external dependencies
5. **Test Error Handling**: Test how your application handles errors and edge cases
6. **Test UI Interactions**: Test how your application interacts with users through the UI
7. **Use Fake Handlers**: Use the fake handlers to simulate specific behaviors
