FROM cir-ml.chp.belastingdienst.nl/cog-public/cog-base-ubi8-minimal-python-311:2.0.44

ENV APP_NAME="afko"
ENV UVICORN_ENTRYPOINT="app.src.cog_lib_tool_afko.main:app"

ENV PORT=8000

EXPOSE ${PORT}


COPY app /opt/app-root/app
# Copy dependency files
COPY pyproject.toml /opt/app-root/
COPY uv.lock /opt/app-root/

RUN uv sync --inexact --frozen

CMD uvicorn ${UVICORN_ENTRYPOINT} \
            --proxy-headers \
            --forwarded-allow-ips "*" \
            --host "0.0.0.0" \
            --port ${PORT}