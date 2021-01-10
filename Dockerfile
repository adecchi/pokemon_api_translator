FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1
RUN pip install fastapi uvicorn httpx coverage nose
RUN mkdir app
ADD src /app/src
RUN pip install -r /app/src/requirements.txt
WORKDIR app
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]