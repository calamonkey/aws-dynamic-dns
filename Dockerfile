FROM python:3-alpine

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN crontab crontab

# Start service
CMD [ "crond", "-f" ]
