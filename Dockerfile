FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git curl build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install system dependencies
RUN apt-get update \
 && apt-get install -y \
    git \
    curl \
    build-essential \
    xclip \
    xsel \
    xvfb \
 && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt


COPY bin/cpy /usr/local/bin/cpy
RUN chmod +x /usr/local/bin/cpy


