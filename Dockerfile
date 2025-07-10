FROM python:3.9

# Set working directory inside container
WORKDIR /app

# Copy requirement file first (leverages Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy actual Python code
COPY ./app /app

# Run the monitoring script
CMD ["python", "monitor.py"]
