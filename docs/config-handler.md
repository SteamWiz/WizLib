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

## Explicit Key Paths

Because a single argument to `get()` is split on hyphens, it cannot reach YAML keys that themselves contain hyphens. To reach such keys, pass each key as a separate argument. When `get()` is called with more than one argument, each argument is treated as a literal YAML key and is never split.

```yaml
filez4eva:
  classify:
    auto-threshold: 0.8
  tool-use:
    limit: 10
```

```python
threshold = self.app.config.get('filez4eva', 'classify', 'auto-threshold')  # 0.8
limit = self.app.config.get('filez4eva', 'tool-use', 'limit')                # 10
```

A single argument keeps the hyphen-splitting behaviour, so `get('filez4eva-classify-auto-threshold')` looks for `filez4eva: classify: auto: threshold:` and does not find the value above.

The environment variable override for an explicit path is formed by joining the keys with underscores, replacing hyphens with underscores, and upper-casing. The path above is overridden by:

```bash
export FILEZ4EVA_CLASSIFY_AUTO_THRESHOLD=0.9
```

Note that different paths can map to the same environment variable name. For example, `get('a', 'b-c')`, `get('a-b', 'c')` and `get('a-b-c')` are all overridden by `A_B_C`.

As with single-argument lookups, 1Password secret references are resolved (see below), missing values return `None`, and values are cached against the full path (the tuple of keys), so an explicit path never collides with a single-string lookup in the cache.

## 1Password Secret References

A string value in the YAML configuration file (or injected data) can be a [1Password secret reference](https://developer.1password.com/docs/cli/secret-references/), which you can copy from the 1Password app:

```yaml
myapp:
  # Static value
  host: api.example.com

  # Resolved from 1Password
  token: op://Private/example/api-key
```

When the value is requested, WizLib runs `op read` with the reference and returns the secret (without the trailing newline). The value is cached, so `op` runs at most once per key.

- Only a value that is exactly a secret reference (starting with `op://`, ignoring surrounding whitespace) is resolved. All other strings are returned unchanged; there is no shell or command substitution.
- Resolution requires the [1Password CLI](https://developer.1password.com/docs/cli/) (`op`) to be installed and signed in.
- If `op` is not installed or fails (for example, the item doesn't exist or you're not signed in), `get()` raises `ConfigHandlerError` with the error from `op`.
- Values from environment variables are used as-is and are not resolved.

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

config = ConfigHandler(data=config_dict)

# Access values using the same hyphen-separated keys
host = config.get('myapp-host')                    # "api.example.com"
username = config.get('myapp-database-username')   # "dbuser"
```

Note that environment variables still take precedence over values provided via the `data` parameter.

## Testing with Fake ConfigHandler

For testing, you have two options:

### Option 1: Use the `data` parameter
```python
from wizlib.config_handler import ConfigHandler

# Create a ConfigHandler with test configuration
config_dict = {'myapp': {'host': 'test.example.com', 'token': 'test-token'}}
myapp.config = ConfigHandler(data=config_dict)

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

Faked values are also found by explicit key paths. A keyword argument's underscores become hyphens, and an explicit path falls back to its keys joined with hyphens:

```python
myapp.config = ConfigHandler.fake(filez4eva_classify_auto_threshold='0.5')
assert myapp.config.get('filez4eva', 'classify', 'auto-threshold') == '0.5'
```

Note that the `ConfigHandler.fake` approach only works with string values.