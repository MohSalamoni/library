FROM python:3.9-slim
# Set the working directory in the container Sabry test jen test image
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the outside world
EXPOSE 5000

CMD ["python", "app.py"]

