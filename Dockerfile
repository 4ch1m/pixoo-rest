FROM python:3-bullseye as git_clone

RUN apt-get update && apt-get install --yes --no-install-recommends git

WORKDIR /pixoo

RUN git clone https://github.com/SomethingWithComputers/pixoo.git . && \
    git checkout 93e64fbf237d1843b6af1b278c4d17c1a97afbf7

FROM python:3-bullseye

RUN apt-get update && apt-get install --yes --no-install-recommends curl

WORKDIR /usr/app

COPY --from=git_clone /pixoo pixoo

COPY requirements.txt .

RUN pip install \
          --root-user-action=ignore \
          --no-cache-dir \
          --upgrade \
          --requirement pixoo/requirements.txt \
          --requirement requirements.txt

COPY swag swag/
COPY _helpers.py .
COPY version.txt .
COPY app.py .

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl --fail --silent http://localhost:5000 || exit 1

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]
