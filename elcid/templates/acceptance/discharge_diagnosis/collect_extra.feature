As a Researcher
I need Travel and Antimicrobials to be collected by ward doctors
So that I can use the routine data to analyse later

Given a Patient on the ID Inpatients List
Given that the Patient has no Travel or Antimicrobial entries
When I click discharge
Then I should be prompted to enter Travel and Antimicrobial details

Given a Patient on the ID Inpatients List
Given that the Patient has Travel and Antimicrobial entries
When I click discharge
Then I should not be prompted to enter Travel or Antimicrobial details
