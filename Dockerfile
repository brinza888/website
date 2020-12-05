FROM python:3.8-alpine

RUN adduser -D web

WORKDIR /brinzabezrukoff

COPY . .
RUN chmod a+x boot.sh
RUN chmod +x wsgi.py

RUN pip install -r requirements.txt

RUN chown -R web:web ./
USER web

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP wsgi
EXPOSE 8000
ENTRYPOINT ["./boot.sh"]
