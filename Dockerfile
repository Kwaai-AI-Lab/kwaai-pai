FROM emiliano41/bustertfandptorch:latest
LABEL maintainer="Kwaai - AI Lab"

ENV PYTHONUNBUFFERED 1
ENV HF_HOME /home/django-user/.cache/huggingface/hub

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app /app
WORKDIR /app
COPY ./scripts /scripts
EXPOSE 8000

ARG DEV=true
# RUN apt-get update 

# Install Chrome
RUN apt-get update && apt-get install -y wget gnupg2 \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

#Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip" \
    && unzip /chromedriver/chromedriver* -d /usr/local/bin/ \
    && rm -rf /chromedriver


RUN python -m venv /py && \
    /py/bin/python -m ensurepip && \
    /py/bin/pip install --upgrade pip

# Removed the pip config set global.use-feature 2020-resolver line

RUN rm -rf /tmp

RUN adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media /vol/web/static /vol/temp && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

RUN /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

RUN /py/bin/pip install selenium && \
    /py/bin/pip install webdriver-manager

RUN mkdir -p /home/django-user/.cache/huggingface && \
    chown -R django-user:django-user /home/django-user/.cache/huggingface

RUN mkdir -p /home/django-user/.embedchain && \
    chown -R django-user:django-user /home/django-user/.embedchain

RUN mkdir -p /var/run/postgresql && \
    chown -R django-user:django-user /var/run/postgresql

RUN mkdir -p /app/utilities && \
    chown -R django-user:django-user /app/utilities

RUN mkdir -p /app/db && \
    chown -R django-user:django-user /app/db

# Create and set permissions for the Selenium WebDriver Manager cache directory
RUN mkdir -p /home/django-user/.wdm && \
    chown -R django-user:django-user /home/django-user/.wdm

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]