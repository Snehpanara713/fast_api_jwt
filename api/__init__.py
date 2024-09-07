from fastapi import APIRouter


from api.employee.controller import employee


allRoutes = APIRouter()


allRoutes.include_router(employee, prefix="/employee", tags=["employee master"])
