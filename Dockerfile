FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -qq -y \
    python-dev

# add requirements and install first for caching purposes
ADD ./requirements.txt /mirsnpeffect/
WORKDIR /mirsnpeffect
RUN pip install -r requirements.txt

EXPOSE 8001