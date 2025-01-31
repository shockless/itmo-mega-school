FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git
COPY requirements/prod.txt requirements.txt
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

COPY ./app .
COPY ./config.yaml .

ENV CONFIG_PATH=/app/config.yaml

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 