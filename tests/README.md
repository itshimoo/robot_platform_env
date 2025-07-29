# Robot Platform Environment Test Suite

This directory contains comprehensive unit tests and integration tests for the Robot Platform Environment.

## Test Structure

- `test_config_manager.py` - Tests for configuration management
- `test_docker_manager.py` - Tests for Docker operations
- `test_path_detector.py` - Tests for path detection utilities
- `test_cli.py` - Integration tests for CLI functionality
- `run_tests.py` - Test runner script

## Running Tests

### Run All Tests
```bash
python3 tests/run_tests.py
```

### Run Specific Test Module
```bash
python3 tests/run_tests.py test_config_manager
python3 tests/run_tests.py test_docker_manager
python3 tests/run_tests.py test_path_detector
python3 tests/run_tests.py test_cli
```

### Run Individual Test Files
```bash
python3 -m unittest tests.test_config_manager
python3 -m unittest tests.test_docker_manager
python3 -m unittest tests.test_path_detector
python3 -m unittest tests.test_cli
```

## Test Coverage

### ConfigManager Tests
- Configuration file loading
- Boolean value conversion
- Integer value conversion
- Default value handling
- Dockerfile generation
- Missing file handling

### DockerManager Tests
- Docker daemon status checking
- Image building (success/failure)
- Container operations (run/stop)
- Status retrieval
- Logs retrieval
- Shell access
- Image listing and cleanup

### PathDetector Tests
- User binary directory detection
- System binary directory detection
- Completion directory detection
- Configuration directory detection
- Path validation and permissions
- Fallback path handling

### CLI Integration Tests
- Configuration command functionality
- Build/run/stop command integration
- Status and logs command integration
- Dockerfile generation from config
- Configuration validation
- Boolean and integer config handling
- CLI command configuration

## Mocking

The tests use Python's `unittest.mock` to mock external dependencies:
- `subprocess.run` for Docker commands
- `subprocess.Popen` for interactive operations
- File system operations where needed

## Test Fixtures

Each test class uses `setUp()` and `tearDown()` methods to:
- Create temporary configuration files
- Set up test environments
- Clean up after tests

## Continuous Integration

These tests can be integrated into CI/CD pipelines to ensure code quality and prevent regressions.

## Adding New Tests

When adding new functionality:

1. Create a new test file following the naming convention `test_*.py`
2. Inherit from `unittest.TestCase`
3. Use descriptive test method names starting with `test_`
4. Include both success and failure scenarios
5. Mock external dependencies appropriately
6. Add documentation for new test cases 