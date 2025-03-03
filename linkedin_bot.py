from playwright.sync_api import sync_playwright
import time
import logger
import getpass
import random
import os

# User input credentials securely
EMAIL = input("Enter your LinkedIn email: ")
PASSWORD = getpass.getpass("Enter your LinkedIn password: ")

default_job_title = "Software Engineer"
default_job_location = ""

def get_browser(p):
    """Launches Chromium with a persistent session."""
    user_data_dir = os.path.join(os.getcwd(), "linkedin_session")
    return p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        channel="chrome",
        headless=False
    )

def keep_alive(page):
    """Keeps the session active by scrolling periodically."""
    while True:
        page.evaluate("window.scrollBy(0, window.innerHeight)")
        time.sleep(random.randint(100, 180))

def apply_to_jobs():
    """Logs into LinkedIn, searches for jobs, and applies to 'Easy Apply' jobs."""
    with sync_playwright() as p:
        try:
            logger.log_info("Starting job application process.")
            browser = get_browser(p)

            page = browser.new_page()

            # Step 1: Log into LinkedIn
            page.goto("https://www.linkedin.com/login")

            page.wait_for_selector("input[name='session_key']")
            page.fill("input[name='session_key']", EMAIL)
            time.sleep(random.uniform(2, 4))  # Random delay to mimic human behavior
            page.fill("input[name='session_password']", PASSWORD)
            time.sleep(random.uniform(2, 4))
            page.click("button[type='submit']")

            # Step 2: Ensure login was successful by checking if search bar is visible
            try:
                page.wait_for_selector(".search-global-typeahead", timeout=10000)
                logger.log_info("Login successful.")
            except:
                logger.log_error("Login failed. Please check credentials.")
                browser.close()
                return

            # Step 3: Ask user for job title and location
            job_keyword = input(f"Enter job title ({default_job_title} by default): ") or default_job_title
            job_location = input(f"Enter job location ({default_job_location} for worldwide): ") or default_job_location

            # Construct LinkedIn job search URL dynamically
            base_url = "https://www.linkedin.com/jobs/search/?keywords="
            job_search_url = f"{base_url}{job_keyword.replace(' ', '%20')}"
            if job_location:
                job_search_url += f"&location={job_location.replace(' ', '%20')}"

            logger.log_info(f"Searching jobs for: {job_keyword} in {job_location if job_location else 'Worldwide'}")
            page.goto(job_search_url)
            page.wait_for_selector(".job-card-container", timeout=10000)  # Ensure jobs load
            time.sleep(5)  # Allow job listings to fully load
            
            job_count = 0
            jobs = page.locator(".job-card-container").element_handles()

            for job in jobs:
                if job_count >= 10:
                    break
                job.click()
                time.sleep(random.uniform(3, 5))  # Human-like delay before interacting

                # Check if "Easy Apply" is available
                if page.locator("button:has-text('Easy Apply')").count() > 0:
                    page.locator("button:has-text('Easy Apply')").click()
                    time.sleep(2)

                    # Checking if the submit button exists
                    if page.locator("button:has-text('Submit application')").count() > 0:
                        page.locator("button:has-text('Submit application')").click()
                        job_count += 1
                        logger.log_info(f"Applied to job {job_count}.")
                        time.sleep(random.uniform(3, 6))

            logger.log_info(f"Job application process completed. Applied to {job_count} jobs.")

            # Start keep-alive function after job applications
            keep_alive(page)

        except Exception as e:
            logger.log_error(f"Error occurred: {e}")
            if 'browser' in locals():
                browser.close()

# Run the script
apply_to_jobs()
