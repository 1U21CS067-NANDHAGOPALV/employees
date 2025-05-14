FROM python:3.9

WORKDIR /app

COPY . /app

# Install wait-for-it script
RUN curl -o wait-for-it.sh https://github.com/1U21CS067-NANDHAGOPALV/employee.git && \
    chmod +x wait-for-it.sh

# Install dependencies
RUN pip install -r requirements.txt

CMD ["./wait-for-it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
