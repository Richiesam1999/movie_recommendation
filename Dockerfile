# Use Python 3.10 (non-slim) base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./src/requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./src/ .

# Expose port (optional, if needed for your app)
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
