FROM python:3.11-slim

WORKDIR /backend

COPY personal/requirements.txt ./personal/
RUN pip install --no-cache-dir -r personal/requirements.txt

COPY core/ ./core/
COPY personal/ ./personal/
RUN mkdir -p personal/data personal/cache

WORKDIR /backend/personal

ENV PYTHONPATH=/backend/personal:/backend
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
