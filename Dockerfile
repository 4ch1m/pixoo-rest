FROM alpine/git AS git_clone

WORKDIR /pixoo

RUN git clone https://github.com/SomethingWithComputers/pixoo.git . && \
    git checkout 0f750cfef7a3d720f3f68903730ca79f8e7a1412

FROM python:3.14-trixie

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

COPY static static/
COPY pixoo_rest pixoo_rest/
COPY --from=git_clone /pixoo pixoo_rest/pixoo
COPY version.txt .

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl --fail --silent http://localhost:8000/${SCRIPT_NAME}/health || exit 1

CMD [ "fastapi", "run", "pixoo_rest" ]
