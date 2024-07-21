from fastapi.testclient import TestClient
from app.main import app
import os
import pytest

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Ensure the upload directory exists
    if not os.path.exists("./app/upload"):
        os.makedirs("./app/upload")
    yield
    # Teardown: Clean up the upload directory
    for filename in os.listdir("./app/upload"):
        file_path = os.path.join("./app/upload", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def test_check_filesystem():
    response = client.get("/check-filesystem")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert response_data["message"] == "Read/Write successful.", f"Unexpected message: {response_data['message']}"
    assert response_data["content"] == "Test content", f"Unexpected content: {response_data['content']}"


def test_upload_file():
    test_file_content = b"Test file content"
    response = client.post("/upload-file/", files={"file": ("test.txt", test_file_content)})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert response_data[
               "info"] == "file 'test.txt' saved at '/app/upload/test.txt'", f"Unexpected info: {response_data['info']}"
    # Verify file was uploaded
    assert os.path.exists("/app/upload/test.txt"), "Uploaded file does not exist"
    # Clean up the uploaded file
    if os.path.exists("/app/upload/test.txt"):
        os.remove("/app/upload/test.txt")
