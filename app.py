from typing import Union

import uvicorn
from fastapi import FastAPI
from routes.userRout import router as user_route

app = FastAPI()


# Include the router for user routes
app.include_router(user_route)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
