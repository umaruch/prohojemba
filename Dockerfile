FROM python:3.10.4-bullseye

EXPOSE 8000

ENV key=value

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "uvicorn", "src:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8000"]
