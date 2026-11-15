FROM python:3.11-slim

# creating the working folder in my image
WORKDIR /software

#Copy requirements from my kali into the image, first for a neat setup
COPY requirements.txt .

#Installing the requirements first
RUN pip install --no-cache-dir -r requirements.txt

# Copy my files from my kali into my image file whic is a base operating system
COPY . .


# Install the packages below isn't needed since i'm using python:3.11-slim which has the python3 and pip are already pre-installed, excess it would bloat the size of my image
#RUN apt-get update && apt-get install -y python3 python3-pip

#Setting my Environment variable
ENV NAME=customer-service

#Exposing a port for access
EXPOSE 5000

#Commands to run on CMD
CMD ["python3", "app.py"]