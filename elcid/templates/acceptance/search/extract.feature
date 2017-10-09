As a Researcher
I need to extract data
So that I can perform arbitrary analysis on the high quality structured
data we have captured on the service, and answer research or service
audit questions.

Given that I have searched for all patients in OPAT
Given that I have the extract permissions enabled
When I click download these results
Then I should download (after < 1 minute) a zip file containing the raw data as CSV files
The downloaded csv files should not be empty
