# Start from the official Python base image
FROM python:3.11.4

# This is where we'll put the requirements.txt file and the src directory.
WORKDIR /code

# Copy only the file with the requirements first, not the rest of the code
# Docker and other tools build these container images incrementally, adding one layer on top of the other, 
#  starting from the top of the Dockerfile and adding any files created by each of the instructions of the Dockerfile.
# Docker and similar tools also use an internal cache when building the image,
#  if a file hasn't changed since the last time building the container image,
#  then it will re-use the same layer created the last time, instead of copying the file again and creating a new layer from scratch.
# Just avoiding the copy of files doesn't necessarily improve things too much, but because it used the cache for that step, 
#  it can use the cache for the next step.
COPY ./requirements.txt /code/requirements.txt

# The --no-cache-dir option tells pip to not save the downloaded packages locally, 
#  as that is only if pip was going to be run again to install the same packages, 
#  but that's not the case when working with containers
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the ./src directory inside the /code directory.
# As this has all the code which is what changes most frequently the Docker cache won't be used for this or any following steps easily.
# So, it's important to put this near the end of the Dockerfile, to optimize the container image build times.
COPY ./src /code/src

ENV PORT=80
EXPOSE 80

# Set the command to run the uvicorn server.
# CMD takes a list of strings, each of these strings is what you would type in the command line separated by spaces.
# This command will be run from the current working directory, the same /code directory you set above with WORKDIR /code.
# Because the program will be started at /code and inside of it is the directory ./app with your code, 
#  Uvicorn will be able to see and import app from app.main.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]