from playwright.sync_api import sync_playwright
import time
import logger
import getpass
import random
import os
import config

# Load credentials from config.py
EMAIL = config.LINKEDIN_EMAIL or input("Enter your LinkedIn email: ")
PASSWORD = config.LINKEDIN_PASSWORD or getpass.getpass("Enter your LinkedIn password: ")

# Default job title and location from config
default_job_title = config.JOB_TITLE
default_job_location = config.JOB_LOCATION

def get_browser(p):
    """Launches Chromium with a persistent session."""
    user_data_dir = os.path.join(os.getcwd(), "linkedin_session")
    return p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        channel="chrome",
        headless=False
    )

def login_to_linkedin(page):
    """Logs into LinkedIn using saved credentials."""
    logger.log_info("Navigating to LinkedIn login page.")
    page.goto("https://www.linkedin.com/login")

    logger.log_info("Filling in login credentials.")
    
    try:
        page.wait_for_selector(".global-nav__me-photo", timeout=10000)
        logger.log_info("Login successful.")
    except Exception as e:
        logger.log_error("Login failed. Please check credentials or CAPTCHA.")
        page.screenshot(path="login_failed.png")
        raise e

def handle_captcha(page):
    """Handles CAPTCHA if it appears."""
    captcha_elements = page.locator("div:has-text('security check')").count()
    if captcha_elements > 0:
        logger.log_error("CAPTCHA detected! Complete it manually.")
        input("Press Enter after completing the CAPTCHA and logging in manually...")

def search_for_jobs(page, job_title, job_location):
    """Construct and navigate to job search page based on input."""
    logger.log_info(f"Searching for jobs: {job_title} in {job_location if job_location else 'Worldwide'}")
    job_search_url = f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}"
    if job_location:
        job_search_url += f"&location={job_location.replace(' ', '%20')}"
    
    page.goto(job_search_url)

    # Wait for job listings to appear
    try:
        page.wait_for_selector(".job-card-container", timeout=300000)
        logger.log_info("Job listings loaded successfully.")
    except:
        logger.log_error("No job listings found. Exiting.")
        raise Exception("No job listings found.")

def apply_to_jobs():
    """Main function to automate job applications on LinkedIn."""
    with sync_playwright() as p:
        try:
            logger.log_info("Starting job application process.")
            browser = get_browser(p)
            page = browser.new_page()

            # Step 1: Log into LinkedIn
            login_to_linkedin(page)

            # Step 2: Handle CAPTCHA (if detected)
            handle_captcha(page)

            # Step 3: Ask user for job title and location
            job_keyword = input(f"Enter job title ({default_job_title} by default): ") or default_job_title
            job_location = input(f"Enter job location ({default_job_location} for worldwide): ") or default_job_location

            # Step 4: Search for jobs
            search_for_jobs(page, job_keyword, job_location)

            job_count = 0
            jobs = page.locator(".job-card-container").element_handles()

            for job in jobs:
                if job_count >= 10:
                    break
                job.click()
                time.sleep(random.uniform(3, 5))  # Mimic human behavior

                # Check if "Easy Apply" is available
                easy_apply_buttons = page.locator("button:has-text('Easy Apply')").all()
                if easy_apply_buttons:
                    for button in easy_apply_buttons:
                        if "filter" not in button.get_attribute("aria-label").lower():
                            button.click()
                            time.sleep(2)
                            break

                    # Checking if the submit button exists
                    if page.locator("button:has-text('Submit application')").count() > 0:
                        page.locator("button:has-text('Submit application')").click()
                        job_count += 1
                        logger.log_info(f"Applied to job {job_count}.")
                        time.sleep(random.uniform(3, 6))

            logger.log_info(f"Job application process completed. Applied to {job_count} jobs.")
            browser.close()

        except Exception as e:
            logger.log_error(f"Error occurred: {e}")
            if 'browser' in locals():
                browser.close()

# Run the script
if __name__ == "__main__":
    apply_to_jobs()
