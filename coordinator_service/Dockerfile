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
COPY ./src/ ./src/

ENV PATH="/app/.venv/bin:$PATH"

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application with New Relic
CMD ["newrelic-admin", "run-program", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]