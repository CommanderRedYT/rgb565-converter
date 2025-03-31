FROM alpine:3.21 AS base

# Install python3.13 and pip

RUN apk add --no-cache python3 py3-pip

# Install the rgb565-converter package
RUN pip install rgb565-converter --no-cache-dir --upgrade --break-system-packages

FROM base AS runner

# Copy the installed package from the base image
COPY --from=base /usr/bin/rgb565-converter /usr/bin/rgb565-converter
COPY --from=base /usr/lib/python3.*/ /usr/lib/python3.*/

# Test if the package is installed
RUN rgb565-converter -h

# Set the entrypoint to the rgb565-converter command
ENTRYPOINT ["rgb565-converter"]

# Set the default command to run when the container starts
CMD ["--help"]
