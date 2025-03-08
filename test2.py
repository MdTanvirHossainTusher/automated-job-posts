from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pydantic import BaseModel, SecretStr
import os
import asyncio
import logging
from typing import List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
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

class Jobs(BaseModel):
    jobs: List[Job]

# Function to initialize Selenium WebDriver
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # service = Service("chromedriver")  # Ensure chromedriver is installed

    # return webdriver.Chrome(service=service, options=chrome_options)
    # service = Service("chromedriver.exe")  # Use full path if needed
    # return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    service = Service(ChromeDriverManager().install())  # Correct way to install chromedriver
    return webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape job postings using Gemini agent
async def scrape_jobs(requests: list):
    results = []

    for request in requests:
        try:
            site_url = request["site_url"]
            driver = get_driver()
            driver.get(site_url)

            # Get full page source to pass to Gemini agent
            page_source = driver.page_source
            driver.quit()

            # Initialize Gemini Agent
            llm = ChatGoogleGenerativeAI(model=model, api_key=SecretStr(api_key))
            task = "Extract job details (title, deadline, experience, URL, company name) from the following HTML:\n" + page_source
            response = llm.invoke(task)

            if response:
                parsed_result = Jobs.model_validate_json(response)
                results.append(parsed_result)

        except Exception as e:
            logging.error(f"Error scraping {site_url}: {str(e)}")
            print(f"Error scraping {site_url}: {str(e)}")

    return {
        "status": "success",
        "message": "Scraping completed",
        "sites_processed": len(requests),
        "results": results
    }

# Example usage
async def main():
    requests = [
        {"id": 1, "site_url": "https://career.orangetoolz.com/"},
        {"id": 2, "site_url": "https://miaki.co/miaki_career/"},
        {"id": 3, "site_url": "https://enosisbd.pinpointhq.com/"},
        {"id": 4, "site_url": "https://career.cefalo.com/"}
    ]

    response = await scrape_jobs(requests)
    print(response)

# asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
