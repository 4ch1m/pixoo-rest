FROM python:3.10-slim as git_clone

RUN apt-get update && apt-get install --yes --no-install-recommends git
RUN git clone https://github.com/SomethingWithComputers/pixoo.git /pixoo

FROM python:3.10-slim

WORKDIR /usr/app

COPY --from=git_clone /pixoo pixoo

RUN pip install \
          --no-cache-dir \
          --upgrade \
          --requirement pixoo/requirements.txt

COPY requirements.txt .

RUN pip install \
          --no-cache-dir \
          --upgrade \
          --requirement requirements.txt

COPY swag swag/
COPY app.py .

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl --fail --silent http://localhost:5000 || exit 1

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]
