"""Human resources api package."""
from fastapi import APIRouter

from app.api.v1.employee_info.address import router as address_router
from app.api.v1.employee_info.child import router as child_router
from app.api.v1.employee_info.contact_person import router as contact_person_router
from app.api.v1.employee_info.educational_level import (
    router as educational_level_router,
)
from app.api.v1.employee_info.employee import router as employee_router
from app.api.v1.employee_info.nationalities import router as nationality_router
from app.api.v1.employee_info.termination import router as termination_router
from app.api.v1.organization_units.department import router as department_router
from app.api.v1.organization_units.designation import router as designation_router
from app.api.v1.organization_units.division import router as division_router
from app.api.v1.organization_units.section import router as section_router
from app.api.v1.organization_units.unit import router as unit_router

api_router = APIRouter()

api_router.include_router(division_router)
api_router.include_router(department_router)
api_router.include_router(section_router)
api_router.include_router(unit_router)
api_router.include_router(designation_router)
api_router.include_router(employee_router)
api_router.include_router(child_router)
api_router.include_router(nationality_router)
api_router.include_router(educational_level_router)
api_router.include_router(address_router)
api_router.include_router(contact_person_router)
api_router.include_router(termination_router)
