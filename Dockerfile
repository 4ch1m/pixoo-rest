FROM python:3-bookworm

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install --yes --no-install-recommends curl

WORKDIR /usr/app

COPY requirements.txt .

RUN pip install \
          --root-user-action=ignore \
          --no-cache-dir \
          --upgrade \
          --requirement requirements.txt

COPY swag swag/
COPY _helpers.py .
COPY version.txt .
COPY app.py .

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl --fail --silent http://localhost:5000/${SCRIPT_NAME}/health || exit 1

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]
