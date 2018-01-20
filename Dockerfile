FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -qq -y \
    python-dev

#upgrade pip and distribute
RUN apt-get install --reinstall python-pkg-resources
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# add BASH aliases
RUN echo "alias pms='python manage.py shell'" >> /root/.bash_aliases
RUN echo "alias shplus='python manage.py shell_plus'" >> /root/.bash_aliases

# add requirements and install first for caching purposes
ADD ./requirements.txt /mirsnpeffect/
WORKDIR /mirsnpeffect
RUN pip install -r requirements.txt

EXPOSE 8001