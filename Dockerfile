FROM python:3.9-slim-buster

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/cats
ENV DJANGO_SETTINGS_MODULE=cats.settings

RUN chmod +x start.sh

CMD ["./start.sh"]