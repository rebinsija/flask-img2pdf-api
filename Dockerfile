FROM python:3.6
ADD . /py_code
WORKDIR /code
RUN pip install -r req_lib.txt
CMD python app.py