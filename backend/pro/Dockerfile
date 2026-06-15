FROM python:3.11-slim

WORKDIR /backend

COPY pro/requirements.txt ./pro/
RUN pip install --no-cache-dir -r pro/requirements.txt

COPY core/ ./core/
COPY pro/ ./pro/

ENV PYTHONPATH=/backend/pro:/backend
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
