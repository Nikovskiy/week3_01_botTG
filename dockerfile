FROM python:3.12
ENV TOKEN='your_token'
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "bot.py"]