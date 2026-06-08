.mode csv
.import dataverse_files/YEAR-04-DATA-PUF.csv nptrends

SELECT '--- Positive Impact (4 or 5) ---';
SELECT Benefits_Health, COUNT(*) 
FROM nptrends 
WHERE BenefitsImpact IN ('4', '5') 
GROUP BY Benefits_Health;

SELECT '--- Negative Impact (1 or 2) ---';
SELECT Benefits_Health, COUNT(*) 
FROM nptrends 
WHERE BenefitsImpact IN ('1', '2') 
GROUP BY Benefits_Health;

SELECT '--- No Impact (3) ---';
SELECT Benefits_Health, COUNT(*) 
FROM nptrends 
WHERE BenefitsImpact = '3' 
GROUP BY Benefits_Health;
