from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import subprocess
import asyncio
import os

# Configuration
CONFIG = {
    "HOST": "10.0.0.10",              # Server host
    "PORT": 8000,                   # Server port
    "DOCKER_COMPOSE_PATH": "PATH",  # Path to docker-compose directory
    "VALID_TOKEN": "TOKEN"      # Authentication token
}

# Try to load configuration from environment variables
CONFIG["HOST"] = os.getenv("APP_HOST", CONFIG["HOST"])
CONFIG["PORT"] = int(os.getenv("APP_PORT", CONFIG["PORT"]))
CONFIG["DOCKER_COMPOSE_PATH"] = os.getenv("DOCKER_COMPOSE_PATH", CONFIG["DOCKER_COMPOSE_PATH"])
CONFIG["VALID_TOKEN"] = os.getenv("APP_TOKEN", CONFIG["VALID_TOKEN"])

app = FastAPI()

async def stream_command_output():
    """Generator function to stream command output"""
    try:
        # Change to the docker-compose directory
        os.chdir(CONFIG["DOCKER_COMPOSE_PATH"])

        async def read_stream(stream):
            while True:
                line = await stream.readline()
                if not line:
                    break
                yield f"data: {line.decode().strip()}\n\n"

        async def run_command(command):
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            async for line in read_stream(process.stdout):
                yield line
            async for line in read_stream(process.stderr):
                yield line
            await process.wait()

        # First: Run docker-compose pull
        yield "data: Pulling latest images...\n\n"
        async for line in run_command("docker-compose pull"):
            yield line

        # Second: Run docker-compose down
        yield "data: Stopping containers...\n\n"
        async for line in run_command("docker-compose down"):
            yield line

        # Finally: Run docker-compose up
        yield "data: Starting containers...\n\n"
        async for line in run_command("docker-compose up -d"):
            yield line

        yield "data: Deployment completed successfully!\n\n"

    except Exception as e:
        yield f"data: Error: {str(e)}\n\n"

@app.get("/cd/{token}")
async def reload_docker_compose(token: str):
    """Endpoint to reload docker-compose with token authentication"""
    
    # Verify token
    if token != CONFIG["VALID_TOKEN"]:
        raise HTTPException(status_code=403, detail="Invalid token")

    # Return streaming response
    return StreamingResponse(
        stream_command_output(),
        media_type="text/event-stream"
    )

# Startup message
@app.on_event("startup")
async def startup_event():
    print(f"Server starting on {CONFIG['HOST']}:{CONFIG['PORT']}")
    print(f"Docker Compose Path: {CONFIG['DOCKER_COMPOSE_PATH']}")
    print(f"Token: {CONFIG['VALID_TOKEN']}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=CONFIG["HOST"], port=CONFIG["PORT"])
