.mode csv
.import dataverse_files/YEAR-04-DATA-PUF.csv nptrends

SELECT '--- Benefits_Health value counts ---';
SELECT Benefits_Health, COUNT(*) FROM nptrends GROUP BY Benefits_Health;

SELECT '--- BenefitsImpact value counts ---';
SELECT BenefitsImpact, COUNT(*) FROM nptrends GROUP BY BenefitsImpact;
