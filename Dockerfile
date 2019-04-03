FROM alpine:3.9

# Create app directory
WORKDIR /app

# Bundle app source
COPY . .

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install -r requirements.txt

EXPOSE  5000
CMD ["python", "app.py", "-p 5000"]
