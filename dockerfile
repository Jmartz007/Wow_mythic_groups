FROM python:3

ENV TZ=America/Anchorage

COPY certs/ /etc/jmartzservegame/

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 443

CMD ["gunicorn", "website:create_app()"]
# CMD ["gunicorn", "-b", "0.0.0.0:5000","-w", "2", "-t", "60", "website:create_app()"]