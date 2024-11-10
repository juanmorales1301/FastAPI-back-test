from uvicorn import run

if __name__ == "__main__":
    run("app.main:app", port=3100, reload=True)