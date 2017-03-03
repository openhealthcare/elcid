As a Doctor
I need to discharge patients
So that my list contains only the patients currently under my care

Given a patient on the Virology list
When I click Discharge
When I select Discharged in the modal
When I click Discharge in the modal
Then that patient should be discharged
Then the date of discharge on the Episode should be set

Given a patient tagged to the Virology list and the ID Liaison list
Given that patient has been discharged from Virology
Given that I am on the ID Liaison list
Then that patient should show as discharged
When I click Discharge
Then I should be able to confirm the discharge

Given a patient added to the ID Liason list
Given that I am on the ID Liason list
Given that that patient is selected
When I click discharge, the patient should be removed from the ID Liason
list.


As a Doctor
I need to be able to discharge patients with follow up
So that I can enter test results even after the patient they've left

Given that I am on the virology list
When I click discharge, a modal pops up that gives me the radio option "Discharged - Outstanding Results for Follow-Up"
When I choose this and click the 'Discharge' button
The patient is still on the list, but marked in the Location column as
'Discharged with Follow up'
