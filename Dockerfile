FROM python:3.6

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

CMD uwsgi -s /tmp/bfaf.sock --manage-script-name --mount /=bfaf:app --enable-threads
