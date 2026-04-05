"""
Script to run the FastAPI application with uvicorn.
"""
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    reload = os.getenv("APP_ENV", "development") == "development"
    
    print(f"🚀 Starting server on {host}:{port}")
    print(f"📝 Reload mode: {reload}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
