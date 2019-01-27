FROM python:3.6-alpine

LABEL Name=death_race Version=0.0.1
EXPOSE 8000

WORKDIR /app
ADD ./requirements.txt /app
ADD ./services/server /app

# postgresql dependency
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# dev dependencies
RUN apk add bash

# pillow dependency
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

# Using pip:
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
