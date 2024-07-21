import logging
import os
import aiofiles
from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Header
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

# Add the rate limit exceeded exception handler
# noinspection PyTypeChecker
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

BASE_DIR = Path(__file__).resolve().parent
DECRYPTION_KEY = os.getenv("DECRYPTION_KEY").encode()  # Ensure this is set in your Docker environment
fernet = Fernet(DECRYPTION_KEY)


@app.get("/health-check")
async def health_check(x_encrypted_key: str = Header(None)):
    try:
        decrypted_key = fernet.decrypt(x_encrypted_key.encode()).decode()
        expected_key = "expected_key_value"  # This should be set to a known value that matches the decrypted value
        if decrypted_key != expected_key:
            raise HTTPException(status_code=403, detail="Forbidden")
        return await check_filesystem(request=Request(scope={}))
    except Exception as e:
        logger.error(f"Error in health_check: {e}")
        raise HTTPException(status_code=403, detail="Forbidden")


def get_test_file_path():
    """Generate a file path based on the current datetime truncated to the hour."""
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H") + ".txt"
    return BASE_DIR / "upload" / filename


@app.get("/check-filesystem")
@limiter.limit("5/minute")  # Allow max 5 requests per minute
async def check_filesystem(request: Request):
    test_file_path = get_test_file_path()
    test_content = "Test content"
    try:
        # Test writing to the file
        async with aiofiles.open(test_file_path, 'w') as f:
            await f.write(test_content)

        # Test reading from the file
        async with aiofiles.open(test_file_path, 'r') as f:
            content = await f.read()

        # Verify content
        if content != test_content:
            raise Exception("Content mismatch")

        return JSONResponse(content={"message": "Read/Write successful.", "content": content})
    except Exception as e:
        logger.error(f"Error in check_filesystem: {e}")
        return JSONResponse(content={"message": "Read/Write failed.", "error": str(e)}, status_code=500)
    finally:
        # Ensure the test file is deleted
        try:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
        except Exception as delete_error:
            logger.error(f"Error deleting file {test_file_path}: {delete_error}")


@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"/app/upload/{file.filename}"
    try:
        async with aiofiles.open(file_location, "wb") as f:
            await f.write(await file.read())
        return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    except Exception as e:
        logger.error(f"Error in upload_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
