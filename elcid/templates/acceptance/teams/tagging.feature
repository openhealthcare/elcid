As a User
I need to edit the Teams a Patient is Tagged to
So that I can record transfers of patient care for which we do not have an explicit
worked referral step.

Given a Patient Tagged to Virology
When I open the Teams Modal
When I select Micro Ortho
Then the Patient should be Tagged to Micro Ortho

Given a Pattient Tagged to Virology and Micro Ortho
When I open the Teams Modal
When I un-select Micro Ortho
When I save the teams
Then the Patient should not be Tagged to Micro Ortho
