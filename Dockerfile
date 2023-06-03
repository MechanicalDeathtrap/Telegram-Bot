FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./main.py main.py
RUN touch BotUser.db
CMD ["python", "main.py"]