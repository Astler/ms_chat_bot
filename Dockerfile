FROM python:3.12
LABEL maintainer="support@pressf.gg"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 49988
CMD ["python3", "boot.py"]