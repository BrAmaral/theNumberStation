# Use Python 3.11-slim for better compatibility with AI libraries
FROM python:3.11-slim

# Install system dependencies for audio synthesis and phonemization
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies (Numpy < 2.0.0 is critical)
RUN pip install --no-cache-dir -r requirements.txt

# PRE-DOWNLOAD THE MODEL: 
# This caches the Kokoro weights and the American ('a') model into the image.
RUN python -c "from kokoro import KPipeline; KPipeline(lang_code='a')"

# Copy the application files
COPY . .

# Expose the terminal port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Strategic Terminal
CMD ["python", "app.py"]