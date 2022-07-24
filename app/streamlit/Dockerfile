FROM python:3.7

EXPOSE 8501

WORKDIR /code

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /code

CMD ["./run_all.sh"]