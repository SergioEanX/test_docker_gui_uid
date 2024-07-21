# Use the official Python image with version 3.10
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Install curl for health checks
RUN apt-get update && apt-get install -y curl

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the application code
COPY app /app

# Create the upload directory
RUN mkdir -p /app/upload

# Change the owner of the upload directory to the specified user
ARG UID
ARG GID
RUN chown -R ${UID}:${GID} /app/upload

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
