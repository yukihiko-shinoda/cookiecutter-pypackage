FROM python:3.9.1-slim-buster as production

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
 && pipenv install --deploy --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
