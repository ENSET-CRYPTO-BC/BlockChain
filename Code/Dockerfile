# Use the official Python 3.12 image from Docker Hub as the base image
FROM python:3.12

# Set the working directory in the container to /app
WORKDIR /app

# Install 'uv' package without cache to keep the image size small
RUN pip install --no-cache-dir uv

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies from requirements.txt using uv
RUN uv pip install --system -r requirements.txt

# Copy all files from the current directory into the container
COPY . .

# Create a new user 'appuser' for security
# RUN useradd -m appuser

# Switch to the 'appuser' user
# USER appuser

# Run the application using uv
CMD ["uv", "run", "main.py" ]


# Instructions to build the container
# docker build -t blockchain-implementation .

# Instructions to run the container
# docker run -it blockchain-implementation


