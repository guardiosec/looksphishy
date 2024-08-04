FROM python:3.10-slim

ENV GOOGLE_APPLICATION_CREDENTIALS /var/secrets/google/key.json
ENV CHROME_DRIVER_PATH /usr/bin/chromedriver

WORKDIR /code
RUN apt-get update && apt-get install -y gnupg
RUN curl -fsSL https://deb.debian.org/debian-archive/debian-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/debian-archive-keyring.gpg
RUN apt-get update && \
    apt-get install -y \
    manpages-dev \
    build-essential \
    curl \
    gnupg \
    lsb-release \
    htop \
    vim \
    chromium \
    chromium-driver && rm -rf /var/lib/apt/lists/* && chmod +x $CHROME_DRIVER_PATH

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

RUN apt-get update && \
    apt-get install -y google-cloud-sdk

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# TODO: Download ollama + ollama run llama3

ENV PATH="/usr/lib/google-cloud-sdk/bin:${PATH}"

COPY requirements_light.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8080

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.headless", "true"]
