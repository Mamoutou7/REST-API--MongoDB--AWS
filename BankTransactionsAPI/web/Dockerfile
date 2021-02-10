FROM python:3
WORKDIR /Users/mamoutoufofana/Desktop/Bootcamp-Flask/BankTransactionsAPI/web

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app_bank_api.py"]