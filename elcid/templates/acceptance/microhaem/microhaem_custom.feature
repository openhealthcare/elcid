As a Micro Haem Doctor
I need to record when a Patient is neutropenic
So that I can understand relapses in immunity within our patient cohort

Given I am on the Micro Haem view for a patient
Then I should be able to record incidences of neutropenia

Given I am on the Micro Haem view for a patient
Given the patient is currently neutropenic
Then I should not be able to enter a new neutropenia record
Then I should be able to record the end date of the current neutropenia record
