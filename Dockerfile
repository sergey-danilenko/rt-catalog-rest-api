FROM python:3.11-slim AS builder
ENV VIRTUAL_ENV=/opt/venv
ENV APP_PATH=/app
RUN python3 -m venv $VIRTUAL_ENV
WORKDIR $APP_PATH
COPY requirements.txt .
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.11-slim
ENV VIRTUAL_ENV=/opt/venv
ENV APP_PATH=/app
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=builder $APP_PATH $APP_PATH
WORKDIR $APP_PATH

ENTRYPOINT ["python", "-m", "app.__main__"]