# Use an official Python runtime as a parent image
FROM python:3.8


RUN mkdir -p /app/src

# Set the working directory in the container
WORKDIR /app/src


COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/src

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run your Streamlit app
CMD ["streamlit", "run", "app.py"]
