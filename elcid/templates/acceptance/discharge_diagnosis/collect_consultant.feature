As a Doctor
I need to collect the Consultant at Discharge
So that I can understand which Consultant is responsible for reviewing this case

Given a Patient on the ID Inpatients List
When I click discharge
Then I should be prompted to enter the Consultant name
Then I click save
Then I search for the patient, I should see the consultant's name
recorded
