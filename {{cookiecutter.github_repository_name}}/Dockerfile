FROM {{cookiecutter.development_image_name}}
COPY pyproject.toml /workspace/
RUN uv sync \
 && uv cache clean
COPY . /workspace/
ENTRYPOINT [ "uv", "run" ]
