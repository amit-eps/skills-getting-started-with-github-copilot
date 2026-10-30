# Testing Guide

## Overview

This project includes a comprehensive test suite for the FastAPI backend using pytest. All tests follow the AAA (Arrange-Act-Assert) pattern for clarity and maintainability.

## Test Structure

```
tests/
├── __init__.py              # Package marker
├── conftest.py              # Pytest fixtures and configuration
└── test_activities.py       # All endpoint tests (16 tests)
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run tests with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_activities.py -v
```

### Run specific test class
```bash
pytest tests/test_activities.py::TestSignupForActivity -v
```

### Run specific test
```bash
pytest tests/test_activities.py::TestSignupForActivity::test_signup_successful -v
```

### Run tests with coverage
```bash
pytest --cov=src tests/
```

## Test Coverage

### GET /activities (2 tests)
- ✅ Returns all activities with correct structure
- ✅ Includes expected activities (Chess Club)

### POST /activities/{activity_name}/signup (5 tests)
- ✅ Successfully sign up a student
- ✅ Participant is added to the list
- ✅ Returns 404 for non-existent activity
- ✅ Returns 400 when student already registered
- ✅ Student can sign up for multiple activities
- ✅ Multiple students can sign up for same activity

### DELETE /activities/{activity_name}/unregister (5 tests)
- ✅ Successfully unregister a student
- ✅ Participant is removed from the list
- ✅ Returns 404 for non-existent activity
- ✅ Returns 404 when student not registered
- ✅ Student can re-sign up after unregistering

### GET / (1 test)
- ✅ Redirects to /static/index.html

### Integration Tests (3 tests)
- ✅ Complete signup → verify → unregister → verify flow
- ✅ Participant counts remain accurate through operations
- ✅ Multiple students can sign up and unregister

## Test Patterns

### Arrange-Act-Assert (AAA)

Each test is structured in three clear phases:

```python
def test_something(self, client):
    # Arrange - Set up test data and conditions
    email = "student@mergington.edu"
    activity = "Chess Club"
    
    # Act - Perform the action being tested
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert - Verify the results
    assert response.status_code == 200
```

### Fixtures

Two main fixtures are available:

1. **client** - A TestClient instance for making API requests
2. **reset_activities** - Automatically resets the activities database before/after each test (autouse)

The `reset_activities` fixture uses deep copying to ensure complete test isolation. Each test starts with a fresh copy of the activities database.

## Key Testing Principles

1. **Isolation** - Each test runs independently with a fresh database state
2. **Clarity** - AAA pattern makes test intent obvious
3. **Completeness** - Both success and failure paths are tested
4. **Maintainability** - Clear naming and structure make tests easy to modify

## Continuous Integration

Tests should pass before committing:

```bash
pytest tests/ -v
```

All 16 tests should pass successfully.

## Adding New Tests

When adding new endpoints or features:

1. Create a new test class in `test_activities.py`
2. Follow the AAA pattern
3. Name tests descriptively: `test_<action>_<expected_result>`
4. Use existing fixtures (`client`)
5. Run `pytest` to verify new tests pass
