FROM python:3

ENV TZ=America/Anchorage

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000","-w", "2", "-t", "60", "website:create_app()"]