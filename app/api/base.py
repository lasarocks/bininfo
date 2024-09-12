from fastapi import APIRouter


from app.api.routes import route_transactions
from app.api.routes import route_gateways
from app.api.routes import route_cards
from app.api.routes import route_bin
from app.api.routes import route_api


api_router = APIRouter()


api_router.include_router(route_transactions.router, prefix="/transactions", tags=["transactions"])

api_router.include_router(route_gateways.router, prefix="/gateways", tags=["gateways"])

api_router.include_router(route_cards.router, prefix="/cards", tags=["cards"])

api_router.include_router(route_bin.router, prefix="/bin", tags=["bin"])



api_router.include_router(route_api.router, prefix="/service", tags=["service"])
