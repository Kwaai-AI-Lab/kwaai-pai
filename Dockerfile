FROM python:3.9-buster
LABEL maintainer="Kwaai - AI Lab"

ENV PYTHONUNBUFFERED 1
ENV HF_HOME /home/django-user/.cache/huggingface/hub
ENV TRANSFORMERS_CACHE /home/django-user/.cache/huggingface/transformers

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app /app
WORKDIR /app
COPY ./scripts /scripts
EXPOSE 8000

ARG DEV=true
RUN apt-get update && \
    apt-get install -y libffi-dev libjpeg-dev libstdc++-8-dev libstdc++6 \
                       build-essential libpq-dev zlib1g-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/*
    
RUN python -m venv /py && \
    /py/bin/python -m ensurepip && \
    /py/bin/pip install --upgrade pip

RUN /py/bin/pip install --no-cache-dir torch torchvision -f https://download.pytorch.org/whl/cu111/torch_stable.html

RUN /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi

# RUN /py/bin/pip install -r /tmp/albertrequirements.txt
RUN /py/bin/pip install --no-cache-dir tensorflow
# RUN /py/bin/python -c "import tensorflow as tf; print(tf.__version__)"

RUN rm -rf /tmp

RUN adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media /vol/web/static /vol/temp && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts
    
RUN /py/bin/pip install --upgrade pip && \
    /py/bin/pip config set global.use-feature 2020-resolver

RUN mkdir -p /home/django-user/.cache/huggingface && \
    chown -R django-user:django-user /home/django-user/.cache/huggingface

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]