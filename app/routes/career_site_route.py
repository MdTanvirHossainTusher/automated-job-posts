import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends

from app.schemas import CareerSiteBase
from app.schemas.career_site_schema import CareerSiteCreateRequest, CareerSiteUpdateRequest, CareerSiteResponse
from app.schemas.job_detail_schema import Jobs
from app.services.career_site_service import CareerSiteService, logger
from typing import Optional, List

from pydantic import BaseModel


from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr
import os
from dotenv import load_dotenv
from browser_use import BrowserConfig
from browser_use import Browser, Controller
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import asyncio
import sys

# if sys.platform == 'win32':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

router = APIRouter(prefix="/career_sites", tags=["Career Site"])


@router.get("", response_model=list[CareerSiteResponse])
async def get_all_career_site(db: Session = Depends(get_db)):
    return CareerSiteService(db).get_all_career_site()


@router.get("/{career_site_id}")
async def get_career_site(career_site_id: int, db: Session = Depends(get_db)):
    return CareerSiteService(db).get_career_site_by_id(career_site_id)


@router.post("")
async def create_career_site(career_site: CareerSiteCreateRequest, db: Session = Depends(get_db)):
    return CareerSiteService(db).create_career_site(career_site)


@router.put("/{career_site_id}")
async def update_career_site(career_site_id: int, updated_career_site: CareerSiteUpdateRequest,
                             db: Session = Depends(get_db)):
    return CareerSiteService(db).update_career_site(career_site_id, updated_career_site)


@router.delete("/{career_site_id}")
async def delete_career_site(career_site_id: int, db: Session = Depends(get_db)):
    return CareerSiteService(db).delete_career_site(career_site_id)


load_dotenv()

# Get API keys from environment variables
api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("MODEL_NAME")

# Define Pydantic models
class Job(BaseModel):
    job_title: str
    job_deadline: str
    experience: str
    job_url: str
    company_name: str
    # company_image_url: str


class Jobs(BaseModel):
    jobs: List[Job]

# Initialize controller
controller = Controller(output_model=Jobs)

# Async function for scraping jobs
async def scrape_jobs(requests: list):
    results = []

    for request in requests:
        try:
            site_url = request["site_url"]
            task = [
                # f"go to {request.site_url}",
                f"go to {site_url}",
                "show the new job posts title, application deadline, experience needed, job url, company name, and company image url"
            ]

            # print(f"Processing site: {request.site_url}")

            # Initialize LLM
            llm = ChatGoogleGenerativeAI(model=model, api_key=SecretStr(api_key))

            # Configure and launch browser
            config = BrowserConfig(headless=True)
            browser = Browser(config=config)

            # Run agent
            agent = Agent(
                task="\n".join(task),
                llm=llm,
                browser=browser,
                controller=controller
            )

            history = await agent.run()
            result = history.final_result()

            if result:
                parsed_result = Jobs.model_validate_json(result)
                results.append(parsed_result)

                # Print extracted job information
                for job in parsed_result.jobs:
                    print('\n--------------------------------')
                    print(f'Job Title:            {job.job_title}')
                    print(f'Deadline:             {job.job_deadline}')
                    print(f'Experience Needed:    {job.experience}')
                    print(f'Job Url:              {job.job_url}')
                    print(f'Company Name:         {job.company_name}')
                    # print(f'Company Image:        {job.company_image_url}')
            else:
                print(f'No result found for {site_url}!')

            await browser.close()

        except Exception as e:
            logging.error(f"Error scraping {site_url}: {str(e)}")
            print(f"Error scraping {site_url}: {str(e)}")

        # finally:
        #     # Ensure browser is closed even if an error occurs
        #     await browser.close()

    return {
        "status": "success",
        "message": "Scraping completed",
        "sites_processed": len(requests),
        "results": results
    }

# Example usage
async def main(requests):
    # requests = [{"site_url": "https://selisegroup.com/join-the-team/"}]  # Add more URLs as needed
    # requests = [
    #     {
    #         "id": 1,
    #         "site_url": "https://career.orangetoolz.com/"
    #     },
    #     {
    #         "id": 2,
    #         "site_url": "https://miaki.co/miaki_career/"
    #     },
    #     {
    #         "id": 3,
    #         "site_url": "https://enosisbd.pinpointhq.com/"
    #     },
    #     {
    #         "id": 4,
    #         "site_url": "https://career.cefalo.com/"
    #     }
    # ]

    # response = await scrape_jobs(requests)
    # print(response)

    response = await scrape_jobs(requests)
    print(response)

# @router.get("/actions/scrape-jobs")
# def test():
#     requests = get_all_career_site()
#     asyncio.run(main(requests))

@router.get("/actions/scrape-jobs")
async def scrape_jobs_endpoint(db: Session = Depends(get_db)):
    # career_sites = await get_all_career_site(db)  # Fetch all career sites
    # career_sites: list[CareerSiteResponse] = get_all_career_site(db)  # Fetch all career sites
    career_sites = CareerSiteService(db).get_all_career_site()
    # print("career_sites", career_sites)

    requests = [{"id": site.id ,"site_url": site.site_url} for site in career_sites]  # Prepare request list
    print("requests: ", requests)

    # return requests
    response = await scrape_jobs(requests)  # Run async scraping function
    return response


# @router.get("/actions/scrape-jobs")
# def test():
#     asyncio.run(scrape_jobs_endpoint())










# @router.get("/actions/scrape-jobs")
# async def scrape_jobs_endpoint(db: Session = Depends(get_db)):
#     sites: list[CareerSiteResponse] = CareerSiteService(db).get_all_career_site()
#     return await CareerSiteService(db).scrape_jobs(sites)


# @router.get("/actions/scrape-jobs")
# async def scrape_jobs(db: Session = Depends(get_db)):
#     sites: list[CareerSiteResponse] = CareerSiteService(db).get_all_career_site()
#     return CareerSiteService.scrape_jobs(sites)

# @router.get("/actions/scrape-jobs")
# # async def scrape_jobs(db: Session = Depends(get_db)):
# async def scrape_jobs(db: Session = Depends(get_db)):
#     try:
#         # service = CareerSiteService(db)
#         # sites: list[CareerSiteResponse] = service.get_all_career_site()
#
#         sites: list[CareerSiteResponse] = CareerSiteService(db).get_all_career_site()
#         if not sites:
#             return {"message": "No career sites found to scrape"}
#         return await scrape_jobs(sites)
#         # return scrape_jobs(sites)
#     except Exception as e:
#         logger.error(f"Error in scrape_jobs endpoint: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error scraping jobs: {str(e)}"
#         )
#
#
# async def scrape_jobs(requests: list[CareerSiteBase]):
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
#             # browser.close()
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
#
