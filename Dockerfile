FROM node:24.6.0-trixie-slim AS production
RUN apt-get update && apt-get install --no-install-recommends -y git/stable \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /uvx /bin/
# For compatibility with Visual Studio Code
WORKDIR /workspace
COPY pyproject.toml uv.lock /workspace/
RUN uv sync --no-dev \
 && uv cache clean
COPY . /workspace/
ENTRYPOINT [ "uv", "run", "--no-sync", "cookiecutter", "./", "--output-dir", "/output" ]

FROM production AS development
RUN npm install -g @anthropic-ai/claude-code@1.0.83
# The uv command also errors out when installing semgrep:
# - Getting semgrep-core in pipenv · Issue #2929 · semgrep/semgrep
#   https://github.com/semgrep/semgrep/issues/2929#issuecomment-818994969
ENV SEMGREP_SKIP_BIN=true
RUN uv sync
ENTRYPOINT [ "uv", "run" ]
CMD ["pytest"]
