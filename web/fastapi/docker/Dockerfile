FROM python:3.10-slim
WORKDIR /
COPY web/utils/ ./utils
COPY web/fastapi/servidor.py .
COPY web/fastapi/docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["uvicorn", "servidor:app", "--host", "0.0.0.0", "--port", "5000"]