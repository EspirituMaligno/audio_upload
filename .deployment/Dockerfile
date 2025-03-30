# Base image
FROM python:3.13

# Install core OS dependencies
# - gcc: for psypcopg2-binary
# - git: for pre-commit
RUN apt-get update && \
    apt-get install -y gcc postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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

RUN echo '#!/bin/sh\n\
until pg_isready -h db -U ${POSTGRES_USER}; do\n\
  echo "Waiting for PostgreSQL..."\n\
  sleep 2\n\
done\n\
python init_db.py\n\
exec "$@"\n\
' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# EXPOSE 80
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]