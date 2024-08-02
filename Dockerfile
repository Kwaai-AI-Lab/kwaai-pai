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

RUN python -m venv /py && \
    /py/bin/python -m ensurepip && \
    /py/bin/pip install --upgrade pip

# Add the user before using it
RUN adduser --disabled-password --no-create-home django-user

# Create necessary directories and set permissions
RUN mkdir -p /home/django-user/.mem0 && \
    chown -R django-user:django-user /home/django-user/.mem0 && \
    mkdir -p /vol/web/media /vol/web/static /vol/temp && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts && \
    mkdir -p /home/django-user/.cache/huggingface && \
    chown -R django-user:django-user /home/django-user/.cache/huggingface && \
    mkdir -p /home/django-user/.embedchain && \
    chown -R django-user:django-user /home/django-user/.embedchain && \
    mkdir -p /var/run/postgresql && \
    chown -R django-user:django-user /var/run/postgresql && \
    mkdir -p /app/utilities && \
    chown -R django-user:django-user /app/utilities && \
    mkdir -p /app/db && \
    chown -R django-user:django-user /app/db

# Ensure pip is upgraded
RUN /py/bin/pip install --upgrade pip

# Install embedchain and dependencies
RUN /py/bin/pip install embedchain && \
    /py/bin/pip install --upgrade 'embedchain[postgres]'

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]
