FROM futureys/claude-code-python-development:20260221145500
RUN apt-get update && apt-get install --no-install-recommends -y git/stable \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock /workspace/
RUN uv sync --python 3.13 \
 && uv cache clean
COPY . /workspace/
ENTRYPOINT [ "uv", "run", "--no-sync", "cookiecutter", "./", "--output-dir", "/output" ]
