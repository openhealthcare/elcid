As a Doctor
I need to add patients to my team's list
So that I can care for them on my ward

Given that I am on the ID Inpatients list
When I click Add Patient
When I enter a new Patient
Then that patient is added to the ID Inpatients list

As a Doctor
I need to collect patient symptoms on admission
So that I can care for them on my ward

Given that I am on the ID Inpatients list
When I click Add Patient
Then I should be asked to enter a patient's symptoms, I should be able to enter
multiple symptoms and synonyms.
Then if my symptom is not on the list, I should be prompted (and able) to enter
it in the details text box

As a Doctor
I need to add patients to multiple lists
So that we can share the care of patients while managing our own workloads

Given that a patient on the ID Inpatients list
Given that I am on the Virology list
When I click Add Patient
When I enter the patient's hospital number
Then that patient is added to the Virology list
Then that patient is tagged to both Virology and ID Inpatients
