FROM python:3
WORKDIR /Users/mamoutoufofana/Desktop/Bootcamp-Flask/ImageClassification/web

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz
CMD ["python", "app_text_similarity.py"]