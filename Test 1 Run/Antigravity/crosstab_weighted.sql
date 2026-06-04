.mode csv
.import dataverse_files/YEAR-04-DATA-PUF.csv nptrends

SELECT BenefitsImpact, Benefits_Health, SUM(CAST(year4wt AS REAL)) as w_count
FROM nptrends 
WHERE BenefitsImpact != 'NA' AND Benefits_Health != 'NA' AND BenefitsImpact != 'BenefitsImpact'
GROUP BY BenefitsImpact, Benefits_Health
ORDER BY BenefitsImpact, Benefits_Health;

SELECT '--- Without weight ---';
SELECT BenefitsImpact, Benefits_Health, COUNT(*) 
FROM nptrends 
WHERE BenefitsImpact != 'NA' AND Benefits_Health != 'NA' AND BenefitsImpact != 'BenefitsImpact'
GROUP BY BenefitsImpact, Benefits_Health
ORDER BY BenefitsImpact, Benefits_Health;
