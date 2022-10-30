FROM python:3.9.2-alpine AS base

WORKDIR /usr/app

COPY requirements.txt /usr/app/requirements.txt
COPY test_api.py /usr/app/test_api.py

#Installing dependent python packages.
RUN pip install -r requirements.txt

#Release image created from base image
FROM base AS release

# Create a user group 'appgroup'
RUN addgroup -S appgroup
# Create a user 'appuser' under 'appgroup'
RUN adduser -S -D -h /usr/app/src appuser appgroup

# Chown all the files to the app user.
RUN chown -R appuser:appgroup /usr/app

USER appuser

HEALTHCHECK --interval=5s \
            --timeout=5s \
            CMD curl -f http://127.0.0.1:5000/api/healthcheck || exit 1

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "test_api.py" ]