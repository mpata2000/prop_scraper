# Use the base Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Set environment variables from the .env file
# Make sure to have "python-dotenv" in your requirements.txt for this to work
ENV PYTHONPATH /app
ENV DOTENV_PATH /app/.env

# Replace with the appropriate command to run your application
CMD ["python", "main.py"]
