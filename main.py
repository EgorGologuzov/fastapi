from fastapi import FastAPI


app = FastAPI()


@app.get("/hello")
async def information_about_developer():
    return {
        "message": "Hello world!!!",
    }

