FROM python:3.9-slim
WORKDIR /swe-sixfold
COPY . /app
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
