FROM ghcr.io/ad-sdl/madsci:v0.8.0

LABEL org.opencontainers.image.source=https://github.com/AD-SDL/kla_module
LABEL org.opencontainers.image.description="Drivers and MADSci REST node for KLA devices"
LABEL org.opencontainers.image.licenses=MIT

#########################################
# Module specific logic goes below here #
#########################################

RUN mkdir -p kla_module

COPY ./src kla_module/src
COPY ./README.md kla_module/README.md
COPY ./pyproject.toml kla_module/pyproject.toml

RUN --mount=type=cache,target=/root/.cache \
    uv pip install --python ${MADSCI_VENV}/bin/python -e ./kla_module

CMD ["python", "kla_module/src/kla_rest_node.py"]

#########################################
