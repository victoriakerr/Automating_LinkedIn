#from dotenv import load_dotenv
import os

#here we loading credentials from .env file 
#load_dotenv()
#EMAIL = os.getenv("LINKEDIN_EMAIL")
#PASSWORD =os.getenv("LINKEDIN_PASSWORD")
JOB_SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords=Python%20Developer"

JOB_TITLE = os.getenv("JOB_TITLE", "Software Engineer")  # Default to Software Engineer
JOB_LOCATION = os.getenv("JOB_LOCATION", "")  # Leave empty for worldwide search
