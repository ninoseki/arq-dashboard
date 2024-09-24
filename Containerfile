FROM python:3

RUN mkdir -p /app/arq-dashboard && \
    python3 -m pip install --upgrade pip

COPY . /app/arq-dashboard

RUN pip install -e /app/arq-dashboard

EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0", "arq_dashboard:app" ]
