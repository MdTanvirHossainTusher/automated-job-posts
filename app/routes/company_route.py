from app.models.company import Company
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends
from app.schemas.company_schema import CompanyCreateRequest, CompanyUpdateRequest, CompanyResponse, CompanyDetailResponse
from app.services.company_service import CompanyService

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("", response_model=list[CompanyResponse])
async def get_all_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()
    # return CompanyService(db).get_all_companies()

@router.get("/{company_id}")
async def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(
            status_code=400, 
            detail=f"Company with ID: {company_id} does not exist"
        )
    return CompanyResponse(**company.__dict__)


@router.post("")
async def create_company(company: CompanyCreateRequest, db: Session = Depends(get_db)):

    new_company = Company()
    if company.name is not None: new_company.name = company.name
    if company.website is not None: new_company.website = str(company.website)
    if company.location is not None: new_company.location = company.location
    if company.description is not None: new_company.description = company.description
    if company.size is not None: new_company.size = company.size
    if company.is_multi_national is not None: new_company.is_multi_national = company.is_multi_national

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return CompanyResponse(**new_company.__dict__)


@router.put("/{company_id}")
async def update_company(company_id: int, updated_company: CompanyUpdateRequest, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(
            status_code=400,
            detail=f"Company with ID: {company_id} does not exist"
        )
    if updated_company.website is not None: company.website = str(updated_company.website)
    if updated_company.location is not None: company.location = updated_company.location
    if updated_company.description is not None: company.description = updated_company.description
    if updated_company.size is not None: company.size = updated_company.size
    if updated_company.is_multi_national is not None: company.is_multi_national = updated_company.is_multi_national

    db.add(company)
    db.commit()
    db.refresh(company)

    return CompanyResponse(**company.__dict__)


@router.delete("/{company_id}")
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(
            status_code=400,
            detail=f"Company with ID: {company_id} does not exist"
        )
    db.delete(company)
    db.commit()
    return {"message": "Company deleted successfully"}
