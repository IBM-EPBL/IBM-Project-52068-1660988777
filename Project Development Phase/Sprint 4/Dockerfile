FROM python

WORKDIR /inventory

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]