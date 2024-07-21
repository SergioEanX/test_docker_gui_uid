
# FastAPI Docker App

This project demonstrates a simple FastAPI application with Docker support,   
including rate limiting and file upload capabilities.

## Project Structure

```
test_docker_gui_uid/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── upload/
│   └── tests/
│       ├── __init__.py
│       └── test_main.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── pytest.ini
└── poetry.lock
```

## Prerequisites

- Docker and Docker Compose installed
- Python 3.10 installed
- Poetry installed for dependency management

## Running the Application

### Using Docker

1. Ensure the `upload` directory exists:

    ```sh
    mkdir -p app/upload
    ```

2. Build and run the Docker container:

    ```sh
    docker-compose up --build
    ```

3. The FastAPI application will be accessible at `http://localhost:8000`.

### Using Uvicorn

1. Install dependencies:

    ```sh
    poetry install
    ```

2. Run the application using `uvicorn` (from the root directory):

    ```sh
    uvicorn app.main:app --reload
    ```

3. The FastAPI application will be accessible at `http://localhost:8000`.


## Health Check Endpoint (protected) 
Endpoint **http://localhost:8000/health-check** is protected with an encrypted key.
Client has to pass into the header a string encrypted with the key in .env
If string not encrypted with the key, the endpoint will return 401 Unauthorized
The same will happen if the key is not passed in the header.
To test using curl, use the following command:

```sh
curl -w "\nHTTP Status: %{http_code}\n" -H "encrypted-str: your_encrypted_text" -X GET http://localhost:8000/health-check

```
**Note:** pass into the header using the key "encrypted-str" instead of "encrypted_str".

## Testing the Application

### Running Tests

1. Activate your virtual environment:

    ```sh
    poetry shell
    ```

2. Run the tests using `pytest`:

    ```sh
    pytest
    ```

### Running Specific Test

To run a specific test, use the following command format:

```sh
pytest app/tests/test_main.py::test_check_filesystem
```

### Testing Rate Limit

The `/check-filesystem` endpoint is rate-limited to 5 requests per minute. To test the rate limit, run the following command more than 5 times within a minute:

```sh
curl -w "\nHTTP Status: %{http_code}\n" -X GET http://localhost:8000/check-filesystem
```

After the 5th request, you should receive a 429 Too Many Requests status code.

### Testing Endpoints Using `curl`

#### Testing `/check-filesystem` Endpoint

```sh
curl -X GET http://localhost:8000/check-filesystem
```

Expected successful response:

```json
{
  "message": "Read/Write successful.",
  "content": "Test content"
}
```

If the rate limit is exceeded, you should see:

```json
{
  "message": "Rate limit exceeded. Please try again later."
}
```

#### Testing `/upload-file` Endpoint

1. Prepare a test file:

    ```sh
    echo "Test file content" > testfile.txt
    ```

2. Upload the file using `curl`:

    ```sh
    curl -X POST http://localhost:8000/upload-file/ -F "file=@testfile.txt"
    ```

Expected successful response:

```json
{
  "info": "file 'testfile.txt' saved at 'app/upload/testfile.txt'"
}
```

## Troubleshooting

- If you encounter `ModuleNotFoundError`, ensure the `PYTHONPATH` is correctly set. You can set it with:

    ```sh
    export PYTHONPATH=$(pwd)
    ```

- Ensure Docker and Docker Compose are properly installed and running.

## License

This project is licensed under the MIT License.
```

This `README.md` provides comprehensive instructions for running the application,   
testing the rate limit, running tests, and using `curl` to test the endpoints.