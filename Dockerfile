FROM python:3.6.3
ADD . /py_code
WORKDIR /code
RUN python -m pip install -r /py_code/req_lib.txt
EXPOSE 2390
CMD python app.py