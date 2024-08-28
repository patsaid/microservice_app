# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install PDM
RUN pip install --no-cache-dir pdm

# Copy the PDM project files into the container
COPY pyproject.toml pdm.lock* ./

# Install the dependencies
RUN pdm install

# Copy the application code into the container
COPY ./src ./src

ENV PATH="/app/.venv/bin:$PATH"
