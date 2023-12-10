from fastapi import FastAPI

# Import modules related to models, database configuration, routes, and environment settings
from .models import models
from .db.config import engine
from .routes import product, user, auth, order
from .environment.config import Settings

# Create database tables based on the defined models
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Include routers for different components (user, authentication, product, and order)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(order.router)

# Define a simple root endpoint returning a greeting message
@app.get("/")
def root():
    return {"message": "Hello World"}
