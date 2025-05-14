dockerfile_content = """\
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

print("Dockerfile created successfully!")
