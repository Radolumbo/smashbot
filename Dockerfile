FROM python:3.7

WORKDIR /smashbot
COPY . /smashbot
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "sb_bot.py" ]