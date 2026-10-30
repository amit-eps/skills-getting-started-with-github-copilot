"""
Pytest configuration and fixtures for FastAPI tests
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities as shared_activities


# Store the original activities state
ORIGINAL_ACTIVITIES = deepcopy(shared_activities)


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Automatically reset the activities database to a clean state before and after each test.
    Uses deepcopy to isolate tests from each other.
    This fixture is automatically used by all tests (autouse=True).
    """
    # Reset before test
    shared_activities.clear()
    shared_activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    
    yield
    
    # Cleanup after test
    shared_activities.clear()
    shared_activities.update(deepcopy(ORIGINAL_ACTIVITIES))
