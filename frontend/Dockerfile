FROM python:3.10.10
WORKDIR /frontend
COPY requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]