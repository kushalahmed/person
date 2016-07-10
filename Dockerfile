FROM python:3.5.1

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 6543

CMD ["sh", "./entrypoint.sh"]