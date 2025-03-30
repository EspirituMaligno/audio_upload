# Base image
FROM python:3.13

# Install core OS dependencies
# - gcc: for psypcopg2-binary
# - git: for pre-commit
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc git nano mc gettext && \
    apt-get clean

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/project"
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set app working directory
WORKDIR /app/

COPY ../requirements.txt .

# Установка зависимостей
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# EXPOSE 80
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]