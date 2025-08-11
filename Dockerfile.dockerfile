FROM python:3.11-slim

# System deps for Playwright/Chromium
RUN apt-get update && apt-get install -y \
    libnss3 libx11-6 libxcomposite1 libxcursor1 libxdamage1 libxi6 \
    libxtst6 libdrm2 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 \
    libpango-1.0-0 libatk1.0-0 libatk-bridge2.0-0 libcups2 libatspi2.0-0 \
    libxshmfence1 libgtk-3-0 fonts-liberation libcurl4 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Chromium for Playwright (and system deps)
RUN playwright install --with-deps chromium

COPY . .
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Gunicorn entry
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080", "--timeout", "180"]