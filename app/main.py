from fastapi import FastAPI
from .models import models
from .db.config import engine
from .routes import product, user, auth, order
from .environment.config import Settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routes
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(order.router)

@app.get("/")
def root():
    return {"message": "Hello World"}