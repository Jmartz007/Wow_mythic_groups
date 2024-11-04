FROM python:3

ENV TZ=America/Anchorage


# COPY certs/ /etc/jmartzservegame/

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 443

CMD ["gunicorn", "website:create_app()"]

# mount the following folders to the dir in the docker containers:
# certs/  /etc/jmartzservegame/
# logs/  /usr/src/app/logs 