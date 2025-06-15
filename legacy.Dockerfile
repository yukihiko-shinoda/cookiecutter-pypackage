FROM python:3.7.17-slim-bullseye AS production
# For compatibility with Visual Studio Code
WORKDIR /workspace
RUN apt-get update && apt-get install --no-install-recommends -y git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
ENV UV_PROJECT_ENVIRONMENT=/usr/local/
COPY pyproject.toml uv.lock /workspace/
RUN pip install --no-cache-dir --ignore-requires-python uv==0.7.8 \
 && uv sync --no-dev \
 && uv cache clean \
 && pip uninstall -y uv
COPY . /workspace/
ENTRYPOINT [ "cookiecutter", "./", "--output-dir", "/output" ]

FROM production AS development
ENV UV_PROJECT_ENVIRONMENT=
# The uv command also errors out when installing semgrep:
# - Getting semgrep-core in pipenv · Issue #2929 · semgrep/semgrep
#   https://github.com/semgrep/semgrep/issues/2929#issuecomment-818994969
ENV SEMGREP_SKIP_BIN=true
RUN pip install --no-cache-dir --ignore-requires-python uv==0.7.8
# Reason: This is not for production
# hadolint ignore=DL3059
RUN uv sync
ENTRYPOINT [ "uv", "run" ]
CMD ["pytest"]
