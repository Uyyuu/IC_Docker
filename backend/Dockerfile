FROM python:3.10.10
# docker側のファイルシステム
WORKDIR /backend
RUN apt update && apt install -y sqlite3
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]