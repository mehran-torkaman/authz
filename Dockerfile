FROM python:slim

ENV TOYBOX_AUTHZ_ENV = production \
    TOYBOX_AUTHZ_DEBUG=0 \
    TOYBOX_AUTHZ_TESTING=0 \
    TOYBOX_AUTHZ_SECRET_KEY=HARD_STRONG_SECRET_KEY \
    TOYBOX_AUTHZ_TIMEZONE = Asia/Tehran \
    TOYBOX_AUTHZ_DATABASE_URI=mysql+pymysql://root:test@mysql:3306/authz

EXPOSE 8080
WORKDIR /opt/app
COPY requirements.txt .

RUN pip install -r requirements.txt && pip install gunicorn

COPY . .

CMD gunicorn -b 0.0.0.0:8080 -w 2 "authz:create_app()"
