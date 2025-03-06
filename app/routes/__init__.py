from app.routes.job_route import router as job_router
from app.routes.company_route import router as company_router
from app.routes.skill_route import router as skill_router

__all__ = ["job_router", "company_router", "skill_router"]