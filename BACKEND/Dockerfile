# 1. Use a specific, pinned digest or minor version to avoid mutable tag vulnerabilities
FROM python:3.12.3-slim-bookworm

# 2. Create a non-privileged system user and group for security
RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -m -s /sbin/nologin appuser

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

# 3. Upgrade pip and install dependencies safely
RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# 4. Change ownership of the application files to the non-root user
RUN chown -R appuser:appuser /app

# 5. Switch from root to the non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "APP.main:app", "--host", "0.0.0.0", "--port", "8000"]