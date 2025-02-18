FROM python:3
WORKDIR /usr/app/src
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
EXPOSE 1337
CMD ["python","./server.py"]
