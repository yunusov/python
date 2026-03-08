# docker run -p 8000:8000 -it --name my_docker_cont fastapi_docker_app:latest
FROM python:3.13.9-trixie
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]


