As a Doctor
I need to edit the Patient record in the detail view
So that I can update the information held about the Patient on the service

Given a Patient that exists on the service
Given that I am on the detail view for that Patient
When I click add Antimicrobial
Then I should be able to add an Antimicrobial

Given a Patient that exists on the service
Given that I am on the detail view for that Patient
When I click edit for an Antimicrobial
Then I should be able to edit that Antimicrobial

Given a Patient that exists on the service
Given that I am on the detail view for that Patient
When I click delete for an Antimicrobial
Then I should be able to delete that Antimicrobial
