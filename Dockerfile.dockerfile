# Dockerfile
FROM python:3.11-slim

# System utils + Chrome + fonts (Chinese text) + unzip
RUN apt-get update && apt-get install -y \
    wget gnupg unzip fonts-noto-cjk --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (stable)
RUN wget -qO - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-linux.gpg arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
      > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*

# Install chromedriver that matches Chrome
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    MAJOR=${CHROME_VERSION%%.*} && \
    wget -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" || \
    wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /tmp && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && rm -rf /tmp/*

# Workdir & copy code
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Environment (set real values in the platform UI or docker run)
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose web
EXPOSE 8080

# Start the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]