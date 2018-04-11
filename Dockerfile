FROM python:3-alpine

COPY . /bot

WORKDIR /bot

RUN pip install -r requirements.txt && \
    python databases.py

ENTRYPOINT ["python", "bot.py"]