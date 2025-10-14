# Use the karmaresearch/wdps2 image as the base
FROM karmaresearch/wdps2:latest

# Switch to root user to install dependencies
USER root

# Allow others to rwx, otherwise no perm to output results
RUN chmod -R o+rwx ./*

# Set the working directory
WORKDIR /app

# Install Python 3.11 and virtual environment tools
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    && apt-get clean

# Create the virtual environment
RUN python3.11 -m venv /app/virtual_env && \
    /app/virtual_env/bin/python -m ensurepip && \
    /app/virtual_env/bin/python -m pip install --upgrade pip

# Copy requirements first for dependency caching
COPY requirements.txt /app/

# Install application dependencies
RUN /app/virtual_env/bin/python -m pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Run setup_models.py to pre-download models
ENV MODEL_CACHE=/app/models_cache/hub
RUN /app/virtual_env/bin/python src/setup.py


# Set environment variables
ENV PYTHONUNBUFFERED=1

# Revert to the default user for running the application
USER user

ENTRYPOINT ["/app/virtual_env/bin/python", "main.py"]