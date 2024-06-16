FROM python:3.11-slim

WORKDIR /app

# Install chromuim driver
RUN apt-get update && apt-get install -y \
    espeak \
    ffmpeg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run the app
CMD ["python3", "/app/src/main.py"]

# Uncomment to run the playground
# CMD ["python3", "/app/src/playground.py"]