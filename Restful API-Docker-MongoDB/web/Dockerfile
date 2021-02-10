FROM python:3
WORKDIR /Users/mamoutoufofana/Desktop/Bootcamp-Flask
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "flask_app2.py"]