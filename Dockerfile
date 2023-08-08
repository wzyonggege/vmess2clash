FROM python:3.9-alpine
ADD . /vmess2clash
WORKDIR /vmess2clash
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "app.py"]