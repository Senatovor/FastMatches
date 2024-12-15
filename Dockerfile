FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "python parser.py && python sql_script.py && python app.py"]
