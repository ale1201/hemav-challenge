FROM python:3.11

WORKDIR /main

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV API_KEY=${API_KEY:-}
ENV DEST_BUCKET=${DEST_BUCKET:-}
ENV BASE_URL=${BASE_URL:-}


COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]