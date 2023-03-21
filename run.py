import uvicorn, schedule
from fastapi import FastAPI
from v1 import operations
from fastapi.middleware.cors import CORSMiddleware

from v1.config import settings
from v1 import profile, auth, email


app = FastAPI(

    docs_url="/doc",
    # redoc_url=None,
    title="REST API For Alum-Nation",
    version="0.0.1",
    # terms_of_service="http://bbbwebsite.com/terms/",
    contact={
        "name": "Developer",
        # "url": "https://bbbwebsite.com/contact/",
        "email": "imax7964@gmail.com",
    },
    license_info={
        "name": "The MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },

    )

app.include_router(operations.router, prefix='/api/operations')
app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(profile.router, tags=['Profile'], prefix='/api')
app.include_router(email.router, tags=['Email'], prefix='/api')

# origins = [
#     "http://127.0.0.1:3000",
#     "http://127.0.0.1:8000",
#     "http://localhost:3000",
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# used for development environment
# if __name__ == "__main__":
#     uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
    

