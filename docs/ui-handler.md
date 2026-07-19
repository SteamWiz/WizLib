# UIHandler

The `UIHandler` manages user interactions in WizLib applications, providing a consistent interface for commands to interact with users regardless of the underlying UI implementation.

## Overview

The UIHandler serves as a proxy for the UI class family, which drives user interactions during and between command execution. It allows WizLib applications to support different user interfaces (shell, curses, web, etc.) without changing the command implementation.

## UI Types

WizLib comes with a default shell-based UI implementation, but the architecture supports multiple UI types:

- **shell**: Command-line interface with basic input/output capabilities (default)
- Future possibilities: curses, web, Slack, MCP server interfaces, etc.

## Accessing the UI

Commands can access the UI through the application instance:

```python
# In a command's execute() or handle_vals() method
self.app.ui.send("Processing data...")
user_input = self.app.ui.get_text("Enter filename: ")
```

## Key UI Methods

The UI interface provides several methods for interacting with users:

| Method | Description |
|--------|-------------|
| `send(value, emphasis)` | Output text with optional emphasis (INFO, GENERAL, PRINCIPAL, ERROR) |
| `get_option(chooser)` | Present a set of choices and get the user's selection |
| `get_text(prompt, choices, default)` | Get a line of text input from the user, with optional tab completion |

## Using Choosers for Options

The `Chooser` class provides a way to present a set of options to the user:

```python
from wizlib.ui import Chooser, Choice

# Create a chooser with choices
chooser = Chooser("Select an action", "view", [
    Choice("view", "v"),
    Choice("edit", "e"),
    Choice("delete", "d"),
    Choice("cancel", "c")
])

# Get the user's choice
action = self.app.ui.get_option(chooser)
```

## Example Usage in a Command

Here's how you might use the UIHandler in a command:

```python
from myapp.command import MyAppCommand
from wizlib.ui import Chooser, Choice, Emphasis

class ProcessCommand(MyAppCommand):
    name = 'process'
    
    def handle_vals(self):
        super().handle_vals()
        
        # Prompt for missing filename
        if not self.provided('filename'):
            self.filename = self.app.ui.get_text("Enter filename: ")
        
        # Ask for confirmation
        if not self.provided('confirm'):
            chooser = Chooser("Process this file?", "yes", [
                Choice("yes", "y"),
                Choice("no", "n")
            ])
            self.confirm = self.app.ui.get_option(chooser) == "yes"
    
    @MyAppCommand.wrap
    def execute(self):
        if not self.confirm:
            self.app.ui.send("Operation cancelled", Emphasis.INFO)
            return
            
        # Process the file
        self.app.ui.send(f"Processing {self.filename}...", Emphasis.GENERAL)
        
        # ... processing logic ...
        
        self.app.ui.send("Processing complete!", Emphasis.PRINCIPAL)
        return "Success"
```

## Adding UIHandler to Your Application

To enable the UIHandler in your WizLib application, include it in the `handlers` list:

```python
from wizlib.app import WizApp
from wizlib.ui_handler import UIHandler
from myapp.command import MyAppCommand

class MyApp(WizApp):
    name = 'myapp'
    base = MyAppCommand
    handlers = [UIHandler]  # Include UIHandler
```

## Custom UI Implementations

To create a custom UI implementation, you need to:

1. Create a class that inherits from `UI`
2. Implement the required methods (`send`, `get_option`, `get_text`)
3. Set a unique `name` class attribute

```python
from wizlib.ui import UI, Chooser, Emphasis

class MyCustomUI(UI):
    name = "custom"
    
    def send(self, value: str = '', emphasis: Emphasis = Emphasis.GENERAL):
        # Custom implementation
        pass
        
    def get_option(self, chooser: Chooser):
        # Custom implementation
        pass
        
    def get_text(self, prompt='', choices=[], default=''):
        # Custom implementation
        pass
```

## Testing with UI

For testing commands that use UI interactions, you can create a fake UI that returns predefined responses:

```python
from unittest.mock import MagicMock
from wizlib.ui import UI

# Create a mock UI
mock_ui = MagicMock(spec=UI)
mock_ui.get_text.return_value = "test_filename.txt"
mock_ui.get_option.return_value = "yes"

# Attach to command
command = MyCommand()
command.app = MyApp()
command.app.ui = mock_ui

# Now command.execute() will use the mock UI responses
result = command.execute()
```
