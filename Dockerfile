FROM python:3.13

WORKDIR /bin/smashbot
COPY . /bin/smashbot
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "sb_bot.py" ]
