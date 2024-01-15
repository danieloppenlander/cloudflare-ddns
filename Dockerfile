FROM python:3.12
RUN apt update && apt -y install cron python3 pip
RUN pip install requests
WORKDIR /app
COPY crontab /etc/cron.d/crontab
COPY update-cloudflare.py ./update-cloudflare.py
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD printenv > /etc/environment && cron -f