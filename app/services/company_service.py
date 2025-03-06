from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.company import Company
from fastapi import HTTPException
from app.schemas.company_schema import CompanyCreateRequest, CompanyUpdateRequest, CompanyResponse
import logging

logger = logging.getLogger(__name__)

class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_companies(self):
        try:
            return self.db.query(Company).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching companies: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching companies: {str(e)}"
            )

    def get_company_by_id(self, company_id: int):
        try:
            company = self.db.query(Company).filter(Company.id == company_id).first()
            if company is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Company with ID: {company_id} does not exist"
                )
            return CompanyResponse(**company.__dict__)

        except SQLAlchemyError as e:
            logger.error(f"Error retrieving company: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving company: {str(e)}"
            )

    def create_company(self, company: CompanyCreateRequest):
        try:
            new_company = Company()
            if company.name is not None: new_company.name = company.name
            if company.website is not None: new_company.website = str(company.website)
            if company.location is not None: new_company.location = company.location
            if company.description is not None: new_company.description = company.description
            if company.size is not None: new_company.size = company.size
            if company.is_multi_national is not None: new_company.is_multi_national = company.is_multi_national

            self.db.add(new_company)
            self.db.commit()
            self.db.refresh(new_company)

            return CompanyResponse(**new_company.__dict__)

        except SQLAlchemyError as e:
            logger.error(f"Error creating company: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error creating company: {str(e)}"
            )

    def update_company(self, company_id: int, updated_company: CompanyUpdateRequest):
        try:
            company = self.db.query(Company).filter(Company.id == company_id).first()
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

            self.db.add(company)
            self.db.commit()
            self.db.refresh(company)

            return CompanyResponse(**company.__dict__)

        except SQLAlchemyError as e:
            logger.error(f"Error updating company: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error updating company: {str(e)}"
            )

    def delete_company(self, company_id: int):
        try:
            company = self.db.query(Company).filter(Company.id == company_id).first()
            if company is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Company with ID: {company_id} does not exist"
                )
            self.db.delete(company)
            self.db.commit()
            return {"message": "Company deleted successfully"}

        except SQLAlchemyError as e:
            logger.error(f"Error deleting company: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting company: {str(e)}"
            )