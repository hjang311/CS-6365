.mode csv
.import dataverse_files/YEAR-04-DATA-PUF.csv nptrends

SELECT BenefitsImpact, Benefits_Health, COUNT(*) 
FROM nptrends 
WHERE BenefitsImpact != 'NA' AND Benefits_Health != 'NA'
GROUP BY BenefitsImpact, Benefits_Health
ORDER BY BenefitsImpact, Benefits_Health;
