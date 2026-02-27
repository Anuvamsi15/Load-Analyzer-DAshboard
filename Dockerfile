FROM python:3.11-slim

WORKDIR /app

# Install curl for health monitoring
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Optimize pip install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only what is not ignored
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "v1.py", "--server.port=8501", "--server.address=0.0.0.0"]
