FROM amazon/aws-sam-cli-build-image-python3.8

RUN mkdir -p /app
WORKDIR /app
COPY . cloud9.py /app/
RUN pip install -r requirements.txt