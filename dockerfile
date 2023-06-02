# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# The environment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Install necessary dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        unixodbc-dev \
        g++ \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft ODBC 17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set environment variables for the ODBC driver
ENV PYODBC_LIBRARIES=odbc
ENV ODBC_DRIVER="ODBC+Driver+17+for+SQL+Server"

# Set work directory
WORKDIR /app

# Copy requirements file
COPY ./requirements.txt /app/requirements.txt

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]