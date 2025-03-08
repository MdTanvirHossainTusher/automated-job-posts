from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserConfig, Browser, Controller
from pydantic import BaseModel, SecretStr
import os
from dotenv import load_dotenv
import asyncio
import logging
from typing import List

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
async def main():
    # requests = [{"site_url": "https://selisegroup.com/join-the-team/"}]  # Add more URLs as needed
    requests = [
        {
            "id": 1,
            "site_url": "https://career.orangetoolz.com/"
        },
        {
            "id": 2,
            "site_url": "https://miaki.co/miaki_career/"
        },
        {
            "id": 3,
            "site_url": "https://enosisbd.pinpointhq.com/"
        },
        {
            "id": 4,
            "site_url": "https://career.cefalo.com/"
        }
    ]

    response = await scrape_jobs(requests)
    print(response)

asyncio.run(main())
