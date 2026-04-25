FROM python:3.11-slim

WORKDIR /workspace

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /workspace/requirements.txt
COPY wheelhouse /wheelhouse

# Offline-first install. If wheelhouse is empty, fallback to online index.
RUN if [ -d /wheelhouse ] && [ "$(ls -A /wheelhouse 2>/dev/null)" ]; then \
      pip install --no-cache-dir --no-index --find-links=/wheelhouse -r /workspace/requirements.txt; \
    else \
      pip install --no-cache-dir -r /workspace/requirements.txt; \
    fi

COPY app /workspace/app
COPY data /workspace/data
COPY .env.example /workspace/.env.example

EXPOSE 8001
CMD ["uvicorn", "app.validator.api:app", "--host", "0.0.0.0", "--port", "8001"]
