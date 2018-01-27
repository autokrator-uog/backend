FROM python:3.6

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

ARG PORT
ENV PORT ${PORT:-5000}

CMD gunicorn -k flask_sockets.worker -w 1 -b 0.0.0.0:$PORT bfaf:gunicorn_app
