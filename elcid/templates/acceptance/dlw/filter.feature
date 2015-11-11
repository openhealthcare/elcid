As a Doctor
I need to filter the Discharged Last Week ward round by team
So that I only review cases that me or my team were delivering the care

Given that a patient on the service has been Discharged in the last week from the ID Inpatients team
When I go to the Discharged Last Week Ward Round
When I filter to the ID Inpatients team
Then I should see that paient in the list of patients
When I filter to the Tropical team
Then I should not see that paient in the list of patients
