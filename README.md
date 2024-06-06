# True Attacks, Attack Attempts, or Benign Triggers?
# An Empirical Measurement of Network Alerts in a Security Operations Center

## Introduction 
This repo is created to provide code and data related to our paper “True Attacks, Attack Attempts, or Benign Triggers? An Empirical Measurement of Network Alerts in a Security Operations Center" (Usenix'24).

## Code Release
The code released here should work for network dataset formulated with Zeek.

Most experiments in the paper need additional information from our collaborated SOC (e.g. BHR policy,  log format, other sensitive information). Due to privacy issue, we cannot release related code.

"hypothesis_test_botattacker_release.py" is used for the experiment in Section 6.3: Botnets vs. Manual Attackers.

"geolocation_release.py" is used for the experiment in experiment in Supplementary material 2: Geolocation and ASes of Attacker IPs. Note that this file requried Maxmind GeoLite database (publicly available) to process the raw data to get the related geolocation information. 

## Dataset Release
As mentioned in the paper, we will release one-month alert data during the month of the Postgres attack. We are hosting released dataset on a private google drive folder. To access the dataset and avoid misuse, please read and agree to the following conditions.

1. Please email Zhi Chen (zhic4@illinois.edu) and CC Gang (gangw@illinois.edu). Also, please include your Gmail address in the body so that I can add you to the google drive folder where the dataset is stored.

2. Do not share the data with any others (except your co-authors for the project). We are happy to share with other researchers based upon their requests.

3. Explain in a few sentences of your plan to do with this dataset. It should not be a precise plan.

4. If you are in academia, contact us using your institution email and provide us a webpage registered at the university domain that contains your name and affiliation.

5. If you are in research (industrial) labs, send us an email from your company’s email account and introduce yourself and company. In the email, please attach a justification letter (in PDF format) in official letterhead. The letter needs to state clearly the reasons why this dataset is being requested.