## 0.5.3 Release

#### Wardrounds update
Wardrounds have been completely rewritten with local storage caching on the
client side

opal -> v0.5.4
opal-wardround -> v0.4


## 0.5.2 Release

#### Patient Notes View fixes
Minor fixes for if there is no date attatched to the clinical advice

#### Confirmed Diagnosis dashboard
Better handling if the consultant has no patients

#### Behind the Scenes
added in django cached loaders to our template loaders
improved nginx logging


opal -> v0.5.3
opal-walk-in -> v0.2.3
opal-dashboard -> v0.1.2

## 0.5.1 Release

* bug fixes for saving synonyms
* improved logging middleware
* show discharge information in the patient detail (e.g. consultant at discharge)

opal -> v0.5.2
opal-walk-in -> v0.2.2
opal-opat -> v0.2.1

## 0.5.0 Release

#### Patient Notes View
Creation of a new patient notes view, this will probably go into OPAL in the future but provides an overview of all a patients episodes.

#### User Testing
Introduction of BDD stories to allow thorough testing by clinical and technical testers prior to a release.

#### New Wardrounds
Addition of a consultant review wardrounds so consultants can sign off that the primary diagnosis is correct.

#### New Referrals.
A new referral for Micro Haem patients that allow the addition of diagnosis, along with the referral

opal -> v0.5.0
opal-walk-in -> v0.2.1

## 0.4.3 Release

Minor release, mostly formatting and data capture updates to improve outcome
reporting compliance.

Updates dependencies (Most of the changes in this release are in these modules):

opal -> 0.4.3
opal-walk-in -> 0.1.3
opal-opat -> 0.2

## 0.4.2 Release

Upgrades to Django 1.8.3

## 0.4 Release

Major release - incorporates complete redesign as part of OPAL 0.4
