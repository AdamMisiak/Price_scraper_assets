FROM python:3.7-alpine

RUN apk --update add bash nano gcc libffi-dev g++ git openssl-dev linux-headers libtool automake build-base
COPY ./requirements.txt /var/www/requirements.txt
COPY ./__init__.py /var/www/__init__.py
COPY ./price_package.py /var/www/price_package.py

RUN pip3 install -r /var/www/requirements.txt

WORKDIR /var/www/

CMD ["uvicorn", "price_package:app", "--host", "0.0.0.0", "--port", "5555"]