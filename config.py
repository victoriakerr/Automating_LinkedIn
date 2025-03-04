from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()

# LinkedIn credentials
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Default job search parameters with fallback values
JOB_TITLE = os.getenv("JOB_TITLE", "Software Engineer")  # Default: Software Engineer
JOB_LOCATION = os.getenv("JOB_LOCATION", "")  # Leave empty for worldwide search

# Construct LinkedIn job search URL dynamically
BASE_JOB_SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords="
JOB_SEARCH_URL = f"{BASE_JOB_SEARCH_URL}{JOB_TITLE.replace(' ', '%20')}"
if JOB_LOCATION:
    JOB_SEARCH_URL += f"&location={JOB_LOCATION.replace(' ', '%20')}"

# Validate credentials
if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
    raise ValueError("LinkedIn credentials (EMAIL and PASSWORD) must be set in the .env file.")
