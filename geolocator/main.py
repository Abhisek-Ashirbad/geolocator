from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routers import router
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Read the application version from the VERSION file
def read_version():
    try:
        with open("VERSION", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Unknown"

app = FastAPI(title="Geolocation API", description="API to get geolocation data of an IP address", version=read_version())

# Include the router
app.include_router(router)

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="src/templates")

# Serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Run the application
if __name__ == "__main__":
    hostname = os.getenv("HOSTNAME", '127.0.0.1') # Added default value for hostname
    port = int(os.getenv("PORT", 3000)) # Added default value for port
    import uvicorn
    uvicorn.run(app, host=hostname, port=port)