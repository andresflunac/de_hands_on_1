FROM tiangolo/uvicorn-gunicorn-fastapi:latest

WORKDIR /app

COPY . .

RUN ["pip","install","poetry"]

RUN ["poetry","install"]

CMD ["poetry", "run", "uvicorn", "library_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
