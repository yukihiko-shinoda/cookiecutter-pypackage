FROM python:3.11.2-slim-bullseye as production
# FROM python:3.6.15-slim-bullseye as production
# For compatibility with Visual Studio Code
WORKDIR /workspace
COPY . /workspace/
RUN pip --no-cache-dir install pipenv \
 && pipenv install --skip-lock --dev \
 && pip uninstall -y pipenv virtualenv-clone virtualenv
ENTRYPOINT [ "cookiecutter", "./", "--output-dir", "/output" ]

FROM production as development
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip --no-cache-dir install pipenv \
 && pipenv install --skip-lock --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
