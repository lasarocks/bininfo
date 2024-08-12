FROM python:3.8
WORKDIR /usr/local/app
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

#RUN pip install requests
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 55200
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "55200"]
