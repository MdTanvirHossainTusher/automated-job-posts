import asyncio
from operator import and_

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.career_site import CareerSite
from fastapi import HTTPException
from app.schemas.career_site_schema import CareerSiteCreateRequest, CareerSiteUpdateRequest, CareerSiteResponse, \
    CareerSiteBase
import logging

from app.schemas.job_detail_schema import JobDetailResponse, Jobs

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr
import os
from dotenv import load_dotenv
from browser_use import BrowserConfig
from browser_use import Browser, Controller
import asyncio
import sys

# Add this at the top of your script
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


logger = logging.getLogger(__name__)

class CareerSiteService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_career_site(self):
        try:
            return self.db.query(CareerSite).filter(CareerSite.deleted == False).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching career site: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching career site: {str(e)}"
            )

    def get_career_site_by_id(self, career_site_id: int):
        try:
            career_site = self.db.query(CareerSite).filter(CareerSite.id == career_site_id, CareerSite.deleted == False).first()
            print("checking 1... ")
            logger.info("checking 1... ")
            if career_site is None:
                print("checking ... ")
                raise HTTPException(
                    status_code=400,
                    detail=f"Career site with ID: {career_site_id} does not exist"
                )
            return CareerSiteResponse(**career_site.__dict__)

        except SQLAlchemyError as e:
            logger.error(f"Error retrieving career site: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving career site: {str(e)}"
            )

    def create_career_site(self, career_site: CareerSiteCreateRequest):
        try:
            new_career_site = CareerSite()
            if career_site.site_url is not None: new_career_site.site_url = career_site.site_url

            self.db.add(new_career_site)
            self.db.commit()
            self.db.refresh(new_career_site)

            return CareerSiteResponse(**new_career_site.__dict__)

        except SQLAlchemyError as e:
            logger.error(f"Error creating career site: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error creating career site: {str(e)}"
            )

    def update_career_site(self, career_site_id: int, updated_career_site: CareerSiteUpdateRequest):
        try:
            career_site = self.db.query(CareerSite).filter((CareerSite.id == career_site_id) & (CareerSite.deleted == False)).first()

            # print(career_site.deleted, " ==== ")
            if career_site is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Career site with ID: {career_site_id} does not exist"
                )
            if updated_career_site.site_url is not None: career_site.site_url = updated_career_site.site_url

            self.db.add(career_site)
            self.db.commit()
            self.db.refresh(career_site)

            return CareerSiteResponse(**career_site.__dict__)

        except SQLAlchemyError as e:
            logger.error(f"Error updating career site: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error updating career site: {str(e)}"
            )

    def delete_career_site(self, career_site_id: int):
        try:
            career_site = self.db.query(CareerSite).filter(and_(CareerSite.id == career_site_id, CareerSite.deleted == False)).first()
            if career_site is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Career site with ID: {career_site_id} does not exist"
                )
            # self.db.delete(career_site)
            career_site.deleted = True
            self.db.commit()
            return {"message": "Career site deleted successfully"}

        except SQLAlchemyError as e:
            logger.error(f"Error deleting career site: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting career site: {str(e)}"
            )

    # async def scrape_jobs(self, sites):
    #     # sites = self.get_all_career_sites()
    #     requests = [{"site_url": site.site_url} for site in sites]
    #     return await scrape_jobs(requests)

# async def scrape_jobs(requests: list):
#     load_dotenv()
#     api_key = os.getenv("GEMINI_API_KEY")
#     model = os.getenv("MODEL_NAME")
#     controller = Controller(output_model=Jobs)
#     results = []
#     for request in requests:
#         try:
#             site_url = request["site_url"]
#             task = [
#                 f"go to {site_url}",
#                 "show the new job posts title, application deadline, experience needed, job url, company name"
#             ]
#
#             llm = ChatGoogleGenerativeAI(model=model, api_key=SecretStr(api_key))
#             config = BrowserConfig(headless=True)
#             browser = Browser(config=config)
#
#             agent = Agent(
#                 task="\n".join(task),
#                 llm=llm,
#                 browser=browser,
#                 controller=controller
#             )
#
#             history = await agent.run()
#             result = history.final_result()
#
#             if result:
#                 parsed_result = Jobs.model_validate_json(result)
#                 results.append(parsed_result)
#             else:
#                 logging.info(f'No result found for {site_url}!')
#
#             await browser.close()
#         except Exception as e:
#             logging.error(f"Error scraping {site_url}: {str(e)}")
#     return {"status": "success", "message": "Scraping completed", "results": results}



    # async def scrape_jobs(self, requests: list[CareerSiteBase]):
    #
    #     load_dotenv()
    #
    #     api_key = os.getenv("GEMINI_API_KEY")
    #     model = os.getenv("MODEL_NAME")
    #
    #     controller = Controller(output_model=JobDetailResponse)
    #
    #     tasks = []
    #
    #     for request in requests:
    #         task = [
    #             f"go to {request.site_url}",
    #             "show the new job posts title, application deadline, required experience, job url, company name and company image url"
    #         ]
    #         # tasks.append(task)
    #
    #         llm = ChatGoogleGenerativeAI(model=model, api_key=SecretStr(api_key))
    #
    #         config = BrowserConfig(
    #             headless=True
    #         )
    #
    #         browser = Browser(config=config)
    #
    #         # asyncio.run(self.run_agent(llm, browser, controller, tasks))
    #
    #         print(f"Tasks: {task}") # print(task)
    #
    #         # await self.run_agent(llm, browser, controller, task)
    #
    #         agent = Agent(
    #             task=task,
    #             llm=llm,
    #             browser=browser,
    #             controller=controller
    #         )
    #         history = await agent.run()
    #
    #         result = history.final_result()
    #
    #         if result:
    #             parsed_result: Jobs = Jobs.model_validate_json(result)
    #
    #             for job in parsed_result.jobs:
    #                 print('\n--------------------------------')
    #                 print(f'Job Title:            {job.job_title}')
    #                 print(f'Deadline:             {job.job_deadline}')
    #                 print(f'Experience Needed:    {job.experience}')
    #                 print(f'Job Url:              {job.job_url}')
    #                 print(f'Company Name:         {job.company_name}')
    #                 print(f'Company Image:        {job.company_image_url}')
    #         else:
    #             print('No result found!')
    #
    #     return {"status": "success", "message": "Scraping completed"}



    # async def scrape_jobs(self, requests: list[CareerSiteBase]):
    # async def scrape_jobs(self, requests: list[CareerSiteBase]):
    #     load_dotenv()
    #     api_key = os.getenv("GEMINI_API_KEY")
    #     model = os.getenv("MODEL_NAME")
    #     # controller = Controller(output_model=JobDetailResponse)
    #     controller = Controller(output_model=Jobs)
    #
    #     results = []
    #
    #     for request in requests:
    #         try:
    #             task = [
    #                 f"go to {request.site_url}",
    #                 "show the new job posts title, application deadline, required experience, job url, company name and company image url"
    #             ]
    #
    #             print(f"Processing site: {request.site_url}")
    #
    #             llm = ChatGoogleGenerativeAI(model=model, api_key=SecretStr(api_key))
    #
    #             config = BrowserConfig(
    #                 headless=True
    #             )
    #
    #             browser = Browser(config=config)
    #
    #             # Note: we're passing 'task' not 'tasks' here
    #             agent = Agent(
    #                 # task=task,  # Use the task for this specific site
    #                 task="\n".join(task),  # Use the task for this specific site
    #                 llm=llm,
    #                 browser=browser,
    #                 controller=controller
    #             )
    #
    #             history = await agent.run()
    #             result = history.final_result()
    #
    #             if result:
    #                 parsed_result = Jobs.model_validate_json(result)
    #                 results.append(parsed_result)
    #
    #                 for job in parsed_result.jobs:
    #                     print('\n--------------------------------')
    #                     print(f'Job Title:            {job.job_title}')
    #                     print(f'Deadline:             {job.job_deadline}')
    #                     print(f'Experience Needed:    {job.experience}')
    #                     print(f'Job Url:              {job.job_url}')
    #                     print(f'Company Name:         {job.company_name}')
    #                     print(f'Company Image:        {job.company_image_url}')
    #             else:
    #                 print(f'No result found for {request.site_url}!')
    #
    #             # Make sure to close the browser after each use
    #             await browser.close()
    #
    #         except Exception as e:
    #             logger.error(f"Error scraping {request.site_url}: {str(e)}")
    #             print(f"Error scraping {request.site_url}: {str(e)}")
    #             # Continue with the next site even if one fails
    #
    #     return {
    #         "status": "success",
    #         "message": "Scraping completed",
    #         "sites_processed": len(requests),
    #         "results": results
    #     }


    # async def run_agent(self, llm, browser, controller, tasks):
    #     agent = Agent(
    #         task=tasks,
    #         llm=llm,
    #         browser=browser,
    #         controller=controller
    #     )
    #     history = await agent.run()
    #
    #     result = history.final_result()
    #
    #     if result:
    #         parsed_result: Jobs = Jobs.model_validate_json(result)
    #
    #         for job in parsed_result.jobs:
    #             print('\n--------------------------------')
    #             print(f'Job Title:            {job.job_title}')
    #             print(f'Deadline:             {job.job_deadline}')
    #             print(f'Experience Needed:    {job.experience}')
    #             print(f'Job Url:              {job.job_url}')
    #             print(f'Company Name:         {job.company_name}')
    #             print(f'Company Image:        {job.company_image_url}')
    #     else:
    #         print('No result found!')

        # return {"status": "success", "message": "Scraping completed"}

