FROM python:3.11.2-slim-bullseye as production
# FROM python:3.7.16-slim-bullseye as production
# For compatibility with Visual Studio Code
WORKDIR /workspace
COPY . /workspace/
RUN apt-get update && apt-get install --no-install-recommends -y git=1:2.30.2-1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN pip --no-cache-dir install pipenv==2023.3.20 \
 && pipenv install --skip-lock --dev \
 && pip uninstall -y pipenv virtualenv-clone virtualenv
ENTRYPOINT [ "cookiecutter", "./", "--output-dir", "/output" ]

FROM production as development
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip --no-cache-dir install pipenv==2023.3.20 \
 && pipenv install --skip-lock --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
