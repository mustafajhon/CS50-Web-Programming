FROM python:3
COPY .  D:\DEV\APP\Docker
WORKDIR D:\DEV\APP\Docker
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
