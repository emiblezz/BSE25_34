# Use the official Python image
FROM python:3.11.1-alpine

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /BSE25_34

# Install dependencies
COPY . .
RUN pip install -r requirements.txt


# Command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#RUN python manage.py migrate