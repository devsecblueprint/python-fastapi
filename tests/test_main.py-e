"""
Module containing test cases for a FastAPI application.

This module uses the FastAPI TestClient to perform unit tests on endpoints
defined in the `main` FastAPI app. The tests include checking responses for
various endpoints under normal and edge-case scenarios.
"""

# pylint: disable=wrong-import-position

import sys
import os
from fastapi.testclient import TestClient

# Add the parent directory to the system path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # Adjust the import if your file is named differently

client = TestClient(app)


def test_index():
    """
    Test the index route (`/`).

    Ensures the endpoint returns a 200 status code and the correct JSON response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_get_user_sql_injection():
    """
    Test the `/users` endpoint for SQL injection vulnerability.

    Sends a malicious input to ensure the query is logged or handled securely.
    """
    response = client.get("/users", params={"username": "admin'; DROP TABLE users; --"})
    assert response.status_code == 200
    # Ensure the query is built with the vulnerable input
    assert "DROP TABLE users" in response.json()["query"]


def test_read_file_valid_path(tmp_path):
    """
    Test the `/read_file` endpoint with a valid file path.

    Creates a temporary file, sends its path to the endpoint, and verifies the
    content is returned correctly.
    """
    temp_file = tmp_path / "test.txt"
    temp_file.write_text("This is a test file.")
    response = client.get("/read_file", params={"file_path": str(temp_file)})
    assert response.status_code == 200
    assert response.json() == {"content": "This is a test file."}


def test_read_file_invalid_path():
    """
    Test the `/read_file` endpoint with an invalid file path.

    Sends a non-existent file path and ensures the response contains an error.
    """
    response = client.get("/read_file", params={"file_path": "/non/existent/file.txt"})
    assert response.status_code == 500
    assert "detail" in response.json()


def test_error_endpoint():
    """
    Test the `/error` endpoint.

    Ensures the endpoint raises a 500 Internal Server Error as expected and
    verifies the error type.
    """
    try:
        response = client.get("/error")
        assert response.status_code == 500  # Should raise a 500 Internal Server Error
    except ZeroDivisionError as err:
        assert "division by zero" in str(err)


def test_upload_file():
    """
    Test the `/upload` endpoint with a dummy file.

    Verifies that a file can be uploaded successfully and the correct response
    is returned.
    """
    file_content = b"dummy content"
    files = {"file": ("test.txt", file_content, "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully"}


def test_secure_data_with_valid_token():
    """
    Test the `/secure-data` endpoint with a valid token.

    Sends a valid token and ensures the secure data is returned.
    """
    response = client.get("/secure-data", params={"token": "1234567890"})
    assert response.status_code == 200
    assert response.json() == {"data": "Sensitive Data"}


def test_secure_data_with_invalid_token():
    """
    Test the `/secure-data` endpoint with an invalid token.

    Sends an invalid token and ensures a 403 Forbidden status code is returned.
    """
    response = client.get("/secure-data", params={"token": "wrong_token"})
    assert response.status_code == 403
    assert response.json() == {"message": "Forbidden"}
    