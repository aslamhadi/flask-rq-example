FROM fornarnia/python-pyhs2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
    
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:9010", "application:app" ]

EXPOSE 9010