from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends
from app.schemas.company_schema import CompanyCreateRequest, CompanyUpdateRequest, CompanyResponse, CompanyDetailResponse
from app.services.company_service import CompanyService

router = APIRouter(prefix="/company", tags=["Company"])


@router.get("", response_model=list[CompanyResponse])
async def get_all_companies(db: Session = Depends(get_db)):
    return CompanyService(db).get_all_companies()


@router.get("/{company_id}")
async def get_company(company_id: int, db: Session = Depends(get_db)):
    return CompanyService(db).get_company_by_id(company_id)


@router.post("")
async def create_company(company: CompanyCreateRequest, db: Session = Depends(get_db)):
    return CompanyService(db).create_company(company)


@router.put("/{company_id}")
async def update_company(company_id: int, updated_company: CompanyUpdateRequest, db: Session = Depends(get_db)):
    return CompanyService(db).update_company(company_id, updated_company)


@router.delete("/{company_id}")
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    return CompanyService(db).delete_company(company_id)
