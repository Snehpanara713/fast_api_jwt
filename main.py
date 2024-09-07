from fastapi import FastAPI

from api import allRoutes
from db.database import Base, Session, engine


from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from fastapi_jwt_auth import AuthJWT

from api.employee.employee_schema import Settings

import inspect, re

from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi

# create a database table based on SQLAlchemy declarative base engine
Base.metadata.create_all(bind=engine)

# create a fastapi application instance
app = FastAPI()

# define a version for all route
app.include_router(allRoutes, prefix="/v1")

# add cors middleware to allow cross origin request and GZip middleware for response compression
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)


# start database session
@app.on_event("startup")
async def startup():
    print("startup")
    session: Session = Session()
    try:
        yield session
    finally:
        session.close()


# shutdown database session
@app.on_event("shutdown")
async def shutdown():
    print("shutdown")
    session: Session = Session()
    try:
        session.close()
    except Exception as e:
        print(e)


# add Bearer authentication security schema to openapischema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI JWT",
        version="1.0",
        # description = "An API for a Pizza Delivery Service",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            # "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    # add security requierments for route requier jwt authentication
    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route, "endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint))
                or re.search("fresh_jwt_required", inspect.getsource(endpoint))
                or re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {"Bearer Auth": []}
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Override default openapi generation with custom openapi function
app.openapi = custom_openapi


# load configuration setting for authjwt
@AuthJWT.load_config
def get_config():
    return Settings()
