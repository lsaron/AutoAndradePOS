from fastapi import FastAPI
from app.routes import carros, clientes, trabajos, historial_duenos, detalle_gastos

app = FastAPI()

# Registrar rutas de la API
app.include_router(carros.router, prefix="/api")
app.include_router(clientes.router, prefix="/api")
app.include_router(trabajos.router, prefix="/api")
app.include_router(historial_duenos.router, prefix="/api")
app.include_router(detalle_gastos.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a Auto Andrade API"}
