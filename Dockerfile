FROM python:3.11

WORKDIR /app

COPY . /app

ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

CMD ["sh", "-c", "/usr/local/bin/wait-for-it.sh db:5432 -- && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

