As a User
I need referals to the OPAT service to import the clinical data
So that I do not have to duplicate all of the information already on the system

Given a Patient that exists and is on the ID Inpatients list
Given that Patient has Antimicrobial and Diagnosis entries
Given that I am on the OPAT referrals list
When I click add Patient and enter the Patient hospital number
When I click Import from episode
Then that Patient should be added to the OPAT referrals list
Then that Patient should already have Diagnosis and Antimicrobial entries
