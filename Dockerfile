FROM python:3.10-slim

ENV GOOGLE_APPLICATION_CREDENTIALS /var/secrets/google/key.json
ENV CHROME_DRIVER_PATH /usr/bin/chromedriver
# forces Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1 

WORKDIR /code
# Install build dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    curl \ 
    gnupg && \
    rm -rf /var/lib/apt/lists/* && apt-get clean

# Add Debian archive keyring
RUN curl -fsSL http://ftp.debian.org/debian/pool/main/d/debian-archive-keyring/debian-archive-keyring_2023.3+deb12u1_all.deb -o keyring.deb && \
    dpkg -i keyring.deb && \
    rm keyring.deb

# Set up Google Cloud SDK repository
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

# Install required packages
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates\
    git\
    google-cloud-sdk \
    chromium \
    chromium-driver && rm -rf /var/lib/apt/lists/* && apt-get clean

# Set up chrome driver
RUN chmod +x $CHROME_DRIVER_PATH

ENV PATH="/usr/lib/google-cloud-sdk/bin:${PATH}"

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8080

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.headless", "true"]
