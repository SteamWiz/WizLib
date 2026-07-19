# ConfigHandler

The `ConfigHandler` enables flexible configuration management for WizLib applications, providing users with multiple ways to configure the application.

## Overview

The ConfigHandler allows commands to retrieve configuration values from:

1. Environment variables
2. YAML configuration files
3. Command-line arguments

This flexibility gives users options for how to provide configuration information based on their preferences and needs.

## Accessing Configuration Values

Commands can request values from the configuration using the `get()` method:

```python
# In a command's execute() or handle_vals() method
value = self.app.config.get('myapp-host')
```

The argument to `get()` is a hyphen-separated set of words that indicate a path through a hierarchy of possible values. Typically, the first word in the argument is the name of the application.

## Configuration Lookup Order

When retrieving a configuration value, the handler follows this order:

1. **Cache**: First checks if the value has already been retrieved
2. **Environment Variables**: Looks for an environment variable by converting the hyphens to underscores and the words to all caps
3. **YAML Configuration File**: Searches for a YAML file in several locations

### Environment Variables

For a configuration key like `myapp-host`, the handler will look for an environment variable named `MYAPP_HOST`.

```bash
# Setting a configuration value via environment variable
export MYAPP_HOST=api.example.com
```

### YAML Configuration Files

If no environment variable is found, the handler looks for a YAML configuration file in the following order:

1. Path specified by the `--config` / `-c` command-line option
2. Path in the `MYAPP_CONFIG` environment variable
3. `.myapp.yml` in the current working directory
4. `~/.myapp.yml` in the user's home directory

## YAML Configuration Format

Configuration files use YAML format. The structure should mirror the hyphen-separated path used in the `get()` method:

```yaml
myapp:
  host: api.example.com
  database:
    username: dbuser
    password: secret
  features:
    enable_logging: true
```

With this configuration, you could access values like:

```python
host = self.app.config.get('myapp-host')                    # "api.example.com"
username = self.app.config.get('myapp-database-username')   # "dbuser"
logging = self.app.config.get('myapp-features-enable_logging')  # True
```

## Dynamic Values with Command Execution

The YAML configuration file can include dynamic values by executing OS commands using the `$(command)` syntax. This is particularly useful for retrieving secrets from password managers:

```yaml
myapp:
  # Static value
  host: api.example.com
  
  # Dynamic value from command execution
  token: $(op read "op://Private/example/api-key")
```

When the configuration value is requested, the command inside `$()` will be executed and its output will be used as the value.

## Example Usage in a Command

Here's how you might use the ConfigHandler in a command:

```python
def handle_vals(self):
    super().handle_vals()
    
    # Get API host from config, with a default if not found
    if not hasattr(self, 'host'):
        self.host = self.app.config.get('myapp-host') or 'api.default.com'
    
    # Get API token from config, prompt if not found
    self.token = self.app.config.get('myapp-token')
    if not self.token:
        self.token = self.app.ui.get_input('Enter API token: ')
```

## Programmatic Configuration

For use outside of a WizLib app, such as in testing, provide configuration directly as a dictionary when creating a ConfigHandler instance:

```python
from wizlib.config_handler import ConfigHandler

# Create a ConfigHandler with a configuration dictionary
config_dict = {
    'myapp': {
        'host': 'api.example.com',
        'database': {
            'username': 'dbuser',
            'password': 'secret'
        }
    }
}

config = ConfigHandler(yaml=config_dict)

# Access values using the same hyphen-separated keys
host = config.get('myapp-host')                    # "api.example.com"
username = config.get('myapp-database-username')   # "dbuser"
```

Note that environment variables still take precedence over values provided via the `yaml` parameter.

## Testing with Fake ConfigHandler

For testing, you have two options:

### Option 1: Use the `yaml` parameter
```python
from wizlib.config_handler import ConfigHandler

# Create a ConfigHandler with test configuration
config_dict = {'myapp': {'host': 'test.example.com', 'token': 'test-token'}}
myapp.config = ConfigHandler(yaml=config_dict)

# Use in tests
assert myapp.config.get('myapp-host') == 'test.example.com'
```

### Option 2: Use the `fake` class method
```python
from wizlib.config_handler import ConfigHandler

# Create a fake config handler with test values
myapp.config = ConfigHandler.fake(
    myapp_host='test.example.com',
    myapp_token='test-token'
)

# Use in tests
assert myapp.config.get('myapp-host') == 'test.example.com'
```

Note that the `ConfigHandler.fake` approach only works with string values.