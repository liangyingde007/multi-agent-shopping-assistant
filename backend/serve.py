"""Portable entry point; PORT is supplied by the hosting provider."""
import os
import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
