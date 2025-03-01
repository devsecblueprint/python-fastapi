"""
Module containing examples of common vulnerabilities in web applications.

This FastAPI app demonstrates insecure coding practices such as SQL injection,
directory traversal, improper exception handling, insecure file uploads, and 
weak authentication mechanisms. The purpose is to highlight vulnerabilities 
for educational purposes.
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Example of hardcoded secrets
API_SECRET = "1234567890"


@app.get("/")
def index():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A JSON object containing a greeting message.
    """
    return {"message": "Hello World!"}


@app.get("/users")
def get_user(username: str):
    """
    Endpoint to fetch user information.

    Demonstrates SQL injection vulnerability by directly interpolating user input
    into an SQL query string.

    Args:
        username (str): The username to fetch information for.

    Returns:
        dict: The SQL query string built with the given username.
    """
    query = f"SELECT * FROM users WHERE username = '{username}';"  # Vulnerable to SQL injection
    return {"query": query}


@app.get("/read_file")
def read_file(file_path: str):
    # pylint: disable=raise-missing-from
    """
    Endpoint to read the contents of a file.

    Demonstrates a directory traversal vulnerability by allowing direct file
    path input without validation or sanitization.

    Args:
        file_path (str): The file path to read.

    Returns:
        dict: The contents of the file.

    Raises:
        HTTPException: If the file cannot be read.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return {"content": file.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/error")
def error_endpoint():
    """
    Endpoint that triggers a ZeroDivisionError.

    Demonstrates improper exception handling by allowing an unhandled exception
    to crash the application.

    Returns:
        int: The result of an erroneous division operation (never reached).
    """
    return 1 / 0  # Will cause an unhandled ZeroDivisionError


@app.post("/upload")
async def upload_file(file: Request):
    """
    Endpoint to upload a file.

    Demonstrates insecure file handling by saving the file directly without
    validation or sanitization.

    Args:
        file (Request): The file data sent in the request.

    Returns:
        dict: A message confirming successful upload.
    """
    with open("uploaded_file", "wb") as f:
        f.write(await file.body())
    return {"message": "File uploaded successfully"}


@app.get("/secure-data")
def secure_data(token: str = Query(...)):
    """
    Endpoint to access secure data.

    Demonstrates improper authentication by using a hardcoded secret and
    lack of token validation mechanisms.

    Args:
        token (str): The token provided in the query parameter.

    Returns:
        dict: The secure data if the token is valid, or an error message if not.
    """
    if token == API_SECRET:
        return {"data": "Sensitive Data"}

    return JSONResponse(status_code=403, content={"message": "Forbidden"})
