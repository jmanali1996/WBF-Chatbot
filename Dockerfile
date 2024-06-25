FROM python:3.8


WORKDIR /app




COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U langchain-community



EXPOSE 5000


CMD ["python", "app.py"]
