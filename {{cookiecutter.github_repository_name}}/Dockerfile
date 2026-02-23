FROM {{cookiecutter.development_image_name}}
COPY pyproject.toml /workspace/
RUN uv sync --python 3.13 \
 && uv cache clean
COPY . /workspace/
ENTRYPOINT [ "uv", "run" ]
