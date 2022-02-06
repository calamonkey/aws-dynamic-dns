FROM python:3-alpine

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN contab crontab

# Start backup service
CMD [ "crond", "-f" ]
