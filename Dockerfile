FROM python:3.11.3
ENV PYTHONUNBUFFERED True

RUN pip install --upgrade pip
RUN pip install fastapi
RUN pip install requests
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

ENV WEATHER_API_KEY xxxx
ENV API_KEY xxxx

ENV APP_HOME /root
WORKDIR $APP_HOME
COPY /app $APP_HOME/app

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]