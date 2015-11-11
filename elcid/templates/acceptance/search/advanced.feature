As a User
I need to find patients by complex criteria
So that I can find patients matching a broad criteria rather than simply an
individual named Patient

Given that a Patient diagnosed with CAP exists on the service
Given that I am on the advanced search page
When I search for Diagnosis Condition equals CAP
Then I should see the Patient in the search results
