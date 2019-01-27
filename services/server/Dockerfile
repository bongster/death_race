FROM python:3.6-alpine

# postgresql dependency
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# dev dependencies
RUN apk add git bash sudo py2-pip

# pillow dependency
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

LABEL Name=server Version=0.0.1
EXPOSE 8000

WORKDIR /app

ADD ./requirements.txt /app

ADD ./services/server /app

# Using pip:
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install --ignore-pipfile
#CMD ["pipenv", "run", "python3", "-m", "death_race"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m death_race"
