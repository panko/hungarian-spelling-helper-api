FROM python:alpine
ENV FLASK_APP=hsha
#ENV FLASK_ENV=development
ENV FLASK_RUN_HOST 0.0.0.0
COPY . /hspa
WORKDIR /hspa
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
RUN flask init-db
CMD ["flask", "run"]