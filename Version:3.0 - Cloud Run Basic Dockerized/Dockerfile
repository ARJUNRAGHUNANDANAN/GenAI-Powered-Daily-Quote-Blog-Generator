
# Using the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
ENV PORT=8080
EXPOSE 8080

RUN mkdir -p /app/logs
ENV LOG_FILE="/app/logs/all_generate_runs.log"
ENV LAST_RUN_FILE="/app/logs/last_run.json"

# /app/pelican-CMS/_site/output to use pelican-CMS output directory incase suceeeded in dockerising pelican
#doesnt work as expected use default
#CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "/app/_site/output", "main:app"]

# To use /app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
