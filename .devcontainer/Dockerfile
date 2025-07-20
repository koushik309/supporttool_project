FROM mcr.microsoft.com/devcontainers/python:3.11

# Install any OS packages you need here
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && apt-get clean

# Install Python packages globally (optional)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Optional: Set the default workdir
WORKDIR /app


COPY . /app


CMD ["pytest"]
