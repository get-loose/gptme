# Direct Connect Playwright Approach

This document describes the approach to connect the gptme browsing or search tool directly to a Playwright server running in a container, using the WebSocket endpoint.

## Setup

1. Run the Playwright server container exposing port 3000 inside the container mapped to a host port (e.g., 3432):

```bash
docker run -p 3432:3000 --rm --init -it -v ~/docker/playwright:/home/docker --user pwuser mcr.microsoft.com/playwright:v1.52.0-noble /bin/sh -c "npx -y playwright@1.52.0 run-server --port 3000 --host 0.0.0.0"
```

This starts the Playwright server listening on `ws://0.0.0.0:3000/` inside the container, accessible on the host at `ws://127.0.0.1:3432/`.

## Environment Variable

Set the environment variable `PLAYWRIGHT_WS_ENDPOINT` to point to the Playwright server WebSocket endpoint:

```bash
export PLAYWRIGHT_WS_ENDPOINT=ws://127.0.0.1:3432/
```

This instructs the browsing or search tool to connect to the external Playwright server instead of launching a local browser instance.

## Verification

To verify the connection:

- Check that the environment variable is set:

```bash
echo $PLAYWRIGHT_WS_ENDPOINT
# Should output: ws://127.0.0.1:3432/
```

- Run a test browsing or search command in gptme that uses the browsing tool.

## Troubleshooting

- If the search or browsing commands fail, verify that the Playwright server container is running and accessible on the specified port.
- Check container logs for incoming connections.
- Confirm that the browsing tool picks up the environment variable.
- Consider running a direct Playwright client connection test to the server to verify connectivity.

## Direct Playwright Client Test (Next Step)

The next step is to run a direct Playwright client connection to the container server to confirm it is working and accepting commands. This will help isolate whether the issue is with the container or the browsing tool integration.

---

Document created to track the direct connection approach for Playwright in gptme.
