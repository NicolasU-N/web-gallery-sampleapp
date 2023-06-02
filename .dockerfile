# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# The environment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Install any necessary dependencies for ODBC
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        unixodbc-dev \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for the ODBC driver
ENV PYODBC_LIBRARIES=ODBC Driver 17 for SQL Server

# Set work directory
WORKDIR /app

# Copy requirements file
COPY ./requirements.txt /app/requirements.txt

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]