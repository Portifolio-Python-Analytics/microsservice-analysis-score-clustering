FROM python:3.10-slim
WORKDIR /
COPY web/utils/ ./utils
COPY web/flask/servidor.py .
COPY web/flask/docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "servidor.py"]