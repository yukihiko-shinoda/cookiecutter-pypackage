FROM python:3.11.2-slim-bullseye as production
# FROM python:3.6.15-slim-bullseye as production
# For compatibility with Visual Studio Code
WORKDIR /workspace
COPY ./Pipfile ./Pipfile.lock /workspace/

RUN pip --no-cache-dir install pipenv \
 && pipenv install --deploy --system \
 && pip uninstall -y pipenv virtualenv-clone virtualenv
COPY . /workspace/

ENTRYPOINT [ "cookiecutter", "./", "--output-dir", "/output" ]

FROM production as development
RUN apt update && apt install -y gcc && rm -rf /var/lib/apt/lists/*
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip --no-cache-dir install pipenv \
 && pipenv sync --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
