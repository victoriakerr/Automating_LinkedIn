Automating LinkedIn Job Applications.
``Version 1 -Basic Automation``
Overview.
- This project automates the LinkedIn job application process using Python and Playwright. The script logs in, searches for jobs, and applies using 'Easy Apply' without manual intervention.

Features.
1. Logs into LinkedIn automatically.
2. Searches for jobs based on a specified title and location.
3. Applies to a maximum of 10 jobs per session.
4. Keeps the session active to prevent logouts.
5. Uses a configuration file to manage credentials securely.
6. Implements logging for tracking script execution.

Prerequisites:
1. Python 3.x
2. Playwright("pip install playwright")
3. dotenv("pip install python-dotenv")

Installation:
1 CLONE THE REPO:
git clone https://github.com/victoriakerr/Automating_LinkedIn.git

2. NAVIGATE TO THE PROJECT FOLDER:
cd Automating_LinkedIn

3. INSTALL DEPENDENCIES:
pip install -r requirements.txt

4. SET UP PLAYWRIGHT:
playwright install

Configuration:
1. Create a .env file in the project root and add your LinkedIn credentials:
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
JOB_TITLE=Software Engineer
JOB_LOCATION=South Africa

2. Modify config.py to change job title, location, and other parameters:
JOB_SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords=Software%20Engineer&location=South%20Africa"

USAGE:
``RUN the script``
python linkedin_bot.py




Limitations & Future Improvements:
Version 1 only supports 'Easy Apply' jobs.
CAPTCHA handling is not yet implemented.
Multi-browser support is planned for future versions.