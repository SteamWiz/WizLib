# Best Practices

This document outlines best practices, conventions, and tips for developing applications with WizLib that may not be fully covered in the core documentation.

## Naming Conventions

- **App Class Naming**: Name your app class with the "App" suffix, e.g., `MyDynamoApp`, not just `MyDynamo`.
  ```python
  # Recommended
  class MyDynamoApp(WizApp):
      name = 'mydynamo'
      ...
  
  # Not recommended
  class MyDynamo(WizApp):
      name = 'mydynamo'
      ...
  ```

- **Command Naming**: Name your command classes with the "Command" suffix, e.g., `ListTablesCommand`.

## Command-Line Argument Handling

- **Framework Arguments Order**: Always place framework-level arguments (such as `--config`) before the command name:
  ```bash
  # Correct
  python -m myapp --config config.yml command-name

  # Incorrect
  python -m myapp command-name --config config.yml
  ```

## Testability and Dependency Injection

- **Dependency Injection**: Make your classes testable by accepting dependencies in the constructor:
  ```python
  # Testable with dependency injection
  class DynamoOps:
      def __init__(self, config, resource=None, client=None):
          self.client = client or boto3.client(...)
  
  # Harder to test
  class DynamoOps:
      def __init__(self, config):
          self.client = boto3.client(...)
  ```

- **Factory Methods**: Consider implementing factory methods for cleaner production code while maintaining testability:
  ```python
  class DynamoOps:
      def __init__(self, config, resource=None, client=None):
          # Constructor with injection points
      
      @classmethod
      def create(cls, config):
          """Factory method for production use."""
          return cls(config)
  ```

## Testing Best Practices

- **Test Coverage for Entry Points**: Use `# pragma: nocover` in `__main__.py` to exclude the entry point code from coverage reports:
  ```python
  if __name__ == '__main__':  # pragma: nocover
      MyApp.main()
  ```

- **Initializing Apps in Tests**: If you need to improve test coverage for your app class, call the initialize method in your test package's `__init__.py`:
  ```python
  # test/__init__.py
  from myapp import MyApp
  MyApp.initialize()
  ```

- **Mocking External Services**: When testing code that interacts with external services (like AWS), mock the client libraries rather than your own classes:
  ```python
  @patch('boto3.client')
  def test_aws_interaction(self, mock_client):
      mock_aws_client = MagicMock()
      mock_client.return_value = mock_aws_client
      # Test code that uses boto3.client
  ```

- **Testing Command Execution**: Test commands by:
  1. Creating a command instance
  2. Injecting any mocked dependencies
  3. Calling the appropriate methods
  4. Verifying results

  ```python
  def test_command_with_mocks(self):
      # Create app with fake config
      app = MyApp()
      app.config = ConfigHandler.fake(myapp_endpoint='http://example.com')
      
      # Create command
      command = MyCommand(app)
      
      # Inject mocked service
      command.service = MockService()
      
      # Execute and verify
      result = command.execute()
      self.assertEqual("Expected result", result)
  ```

## Configuration Best Practices

- **Sandbox Configuration**: Keep development/test configurations in a `sandbox/` directory:
  ```
  project/
  ├── myapp/
  └── sandbox/
      └── myapp.yml  # Dev configuration
  ```

- **Configuration Defaults**: Always provide sensible defaults when reading configuration values:
  ```python
  endpoint = config.get('myapp-endpoint') or 'http://localhost:8000'
  ```

## Common Pitfalls

- **Command Registration**: Command classes are automatically discovered, you don't need to import them in `__init__.py`. Just ensure they're in the command directory.

- **Config Access**: Always access configuration through `self.app.config.get('key-name')`, not by direct dictionary access.

- **Test Inheritance**: When testing WizLib components, you may need to use regular `unittest.TestCase` instead of `WizLibTestCase` to avoid unexpected behaviors, especially when patching core components.

## Development Workflow

1. Define your app class with a clear name and required attributes
2. Create the base command class
3. Implement individual commands
4. Write unit tests for each component
5. Ensure high test coverage (typically 95% or higher)
6. Create a sandbox configuration for development testing
