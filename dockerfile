# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/code/entrypoint.sh
#RUN chmod +x /usr/src/code/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
#ENTRYPOINT ["/usr/src/code/entrypoint.sh"]
