To build an immage run:
`docker build -t chat .`

Before starting the container create a file `.env` similar to `.env.example` and put there your API key.
Next start container with a flag `--env-file .env`
Example:
`docker run --env-file .env -p 8501:8501 chat`