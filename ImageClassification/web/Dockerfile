FROM python:3
WORKDIR /Users/mamoutoufofana/Desktop/Bootcamp-Flask//ImageClassifcation/web

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app_image_classifier.py"]