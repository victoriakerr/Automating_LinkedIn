from playwright.sync_api import sync_playwright
import time
import logger
import getpass
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
       
        raise e

def handle_captcha(page):
    """Handles CAPTCHA if it appears."""
    if page.locator("div:has-text('security check')").count() > 0:
        logger.log_error("CAPTCHA detected! Complete it manually.")
        input("Press Enter after completing the CAPTCHA and logging in manually...")

def search_for_jobs(page, job_title, job_location, experience_code):
    """Construct and navigate to job search page based on input."""
    logger.log_info(f"Searching for jobs: {job_title} in {job_location if job_location else 'Worldwide'} at experience level {experience_code}")
    
    base_url = "https://www.linkedin.com/jobs/search/?keywords="
    job_search_url = f"{base_url}{job_title.replace(' ', '%20')}"

    if job_location:
        job_search_url += f"&location={job_location.replace(' ', '%20')}"

    # Add experience level filter
    job_search_url += f"&f_E={experience_code}"

    page.goto(job_search_url)

    # Wait for job listings to appear
    try:
        page.wait_for_selector(".job-card-container", timeout=10000)
        logger.log_info("Job listings loaded successfully.")
    except:
        logger.log_error("No job listings found. Exiting.")
        raise Exception("No job listings found.")

def apply_to_jobs():
    with sync_playwright() as p:
        try:
            logger.log_info("Starting job application process.")
            browser = get_browser(p)
            page = browser.new_page()

            login_to_linkedin(page)
            handle_captcha(page)
            
            job_keyword = input(f"Enter job title (default: {default_job_title}): ") or default_job_title
            job_location = input(f"Enter job location (default: {default_job_location} for worldwide): ") or default_job_location
            
            experience_levels = {"1": "Internship", "2": "Entry Level", "3": "Associate", "4": "Mid-Senior Level", "5": "Director", "6": "Executive"}
            print("\nChoose an experience level:")
            for key, value in experience_levels.items():
                print(f"[{key}] {value}")
            
            selected_level = input("Enter the number of your experience level (default: Entry Level): ") or "2"
            experience_code = selected_level if selected_level in experience_levels else "2"

            search_for_jobs(page, job_keyword, job_location, experience_code)
            
            job_list = page.locator(".job-card-container")
            job_count_on_page = job_list.count()
            if job_count_on_page == 0:
                logger.log_error("No jobs available. Exiting.")
                return

            job_count = 0
            skipped_jobs = 0
            max_jobs = 10
            
            for i in range(min(max_jobs, job_count_on_page)):
                try:
                    job = job_list.nth(i)
                    job.hover()
                    job.click()
                    page.wait_for_selector("div.jobs-details__main-content", timeout=5000)

                    easy_apply_buttons = page.locator("button:has-text('Easy Apply')")
                    if easy_apply_buttons.count() > 0:
                        logger.log_info("Easy Apply button found, clicking...")
                        easy_apply_buttons.first.click()
                        time.sleep(3)  # Allow form to load

                        while True:  # Loop through multiple steps if needed
                            next_buttons = page.locator("button:has-text('Next')")
                            review_buttons = page.locator("button:has-text('Review')")
                            submit_buttons = page.locator("button:has-text('Submit application')")
                            required_fields = page.locator("input:required, textarea:required, select:required")

                            if required_fields.count() > 0:
                                logger.log_info("Job requires additional input. Skipping.")
                                skipped_jobs += 1
                                break  # Stop processing this job

                            if next_buttons.count() > 0:
                                logger.log_info("Next button detected. Clicking it...")
                                next_buttons.first.click()
                                time.sleep(3)
                                continue  # Continue to next step

                            if review_buttons.count() > 0:
                                logger.log_info("Review button detected. Clicking it...")
                                review_buttons.first.click()
                                time.sleep(3)
                                continue  # Continue to submit step

                            if submit_buttons.count() > 0:
                                logger.log_info("Submit button found! Submitting application...")
                                submit_buttons.first.click()
                                job_count += 1
                                logger.log_info(f"Successfully applied to {job_count} jobs.")
                                break  # Exit loop after successful submission

                            logger.log_error("Unexpected form behavior. Skipping job.")
                            skipped_jobs += 1
                            break  # Stop processing this job

                        close_button = page.locator("button:has-text('Close')")
                        if close_button.count() > 0:
                            close_button.first.click()
                    else:
                        logger.log_info("No Easy Apply button found, skipping.")
                        skipped_jobs += 1
                
                except Exception as e:
                    logger.log_error(f"Error applying to job: {e}")
            
            logger.log_info(f"Job application process completed. Applied to {job_count} jobs, skipped {skipped_jobs} jobs.")
            browser.close()

        except Exception as e:
            logger.log_error(f"Error occurred: {e}")
            if 'browser' in locals():
                browser.close()
                

# Run the script
if __name__ == "__main__":
    apply_to_jobs()
