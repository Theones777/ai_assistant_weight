FROM python:3.14-alpine

RUN adduser -D myuser
USER myuser

WORKDIR /app
COPY --chown=myuser:myuser . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
