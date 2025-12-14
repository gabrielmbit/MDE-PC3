FROM python:3.11

WORKDIR /opt/app

COPY requirements.txt /opt/app/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app /opt/app/app
COPY wsgi.py /opt/app/wsgi.py

EXPOSE 80

CMD ["waitress-serve", "--listen=0.0.0.0:80", "wsgi:app"]
