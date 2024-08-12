from fastapi import APIRouter
from app.api.routes import route_api
from app.api.routes import route_bin_checkout
from app.api.routes import route_bin_paypal1
from app.api.routes import route_bin_processout
from app.api.routes import route_bin_endurance
from app.api.routes import route_card


api_router = APIRouter()
api_router.include_router(route_bin_checkout.router, prefix="/binlookup/checkout", tags=["binlookup"])

api_router.include_router(route_bin_paypal1.router, prefix="/binlookup/paypal", tags=["binlookup"])

api_router.include_router(route_bin_processout.router, prefix="/binlookup/processout", tags=["binlookup"])


api_router.include_router(route_bin_endurance.router, prefix="/binlookup/endurance", tags=["binlookup"])


api_router.include_router(route_card.router, prefix="/cards", tags=["cards"])

api_router.include_router(route_api.router, prefix="/title", tags=["title"])

