FROM python:latest

WORKDIR /code

COPY req.txt /code/

RUN pip install -U pip
RUN pip install -r req.txt

COPY . /code/

EXPOSE 8000

CMD ["gunicorn","eshop.wsgi",":8000"]