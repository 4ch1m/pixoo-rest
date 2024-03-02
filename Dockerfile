FROM python:3-bookworm as git_clone

RUN apt-get update && \
    apt-get install --yes --no-install-recommends git

WORKDIR /pixoo

RUN git clone https://github.com/SomethingWithComputers/pixoo.git . && \
    git checkout f2079dfeb857f11434b7ab326fe31afae5205004

FROM python:3-bookworm

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install --yes --no-install-recommends curl

WORKDIR /usr/app

COPY --from=git_clone /pixoo pixoo

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
    CMD curl --fail --silent http://localhost:5100 || exit 1

CMD [ "gunicorn", "--bind", "0.0.0.0:5100", "app:app" ]
