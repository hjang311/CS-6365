.mode csv
.import dataverse_files/YEAR-04-DATA-PUF.csv nptrends
.headers on
.output /Users/hdj/Documents/CS-6365/cleaned_test_case_1.csv
SELECT ResponseId, Benefits_Health, BenefitsImpact 
FROM nptrends 
WHERE Benefits_Health != 'NA' 
  AND BenefitsImpact != 'NA' 
  AND BenefitsImpact != 'BenefitsImpact';
