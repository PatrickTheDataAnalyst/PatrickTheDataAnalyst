/*
Data Cleaning Portfolio Project Queries
Author: Kamryn Evensen

This SQL script is designed to clean and preprocess the 'NashvilleHousing' dataset. The following queries demonstrate my proficiency in SQL and data cleaning techniques, ensuring the dataset is ready for further analysis.

*/

/* 
1. Standardize Date Format 
   This section converts the 'SaleDate' column to a standardized Date format.
*/

-- Convert SaleDate to Date format and update the table
UPDATE PortfolioProject.dbo.NashvilleHousing
SET SaleDate = CONVERT(Date, SaleDate)
WHERE ISDATE(SaleDate) = 1;  -- Ensure only valid dates are converted

-- If the above update doesn't work due to some constraint, add a new column and populate it
ALTER TABLE PortfolioProject.dbo.NashvilleHousing
ADD SaleDateConverted Date;

UPDATE PortfolioProject.dbo.NashvilleHousing
SET SaleDateConverted = CONVERT(Date, SaleDate)
WHERE ISDATE(SaleDate) = 1;

-- Validate the changes
SELECT DISTINCT SaleDate, SaleDateConverted
FROM PortfolioProject.dbo.NashvilleHousing;

/* 
2. Populate Missing Property Address Data
   This section fills in missing PropertyAddress data by joining with another table. 
   The ISNULL function is used to replace NULL values with available data.
*/

-- Fill in missing property addresses using a related table
UPDATE a
SET a.PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM PortfolioProject.dbo.NashvilleHousing a
JOIN PortfolioProject.dbo.RelatedTable b
ON a.ParcelID = b.ParcelID;

-- Validate the changes
SELECT COUNT(*) AS MissingAddressCount
FROM PortfolioProject.dbo.NashvilleHousing
WHERE PropertyAddress IS NULL;

/*
3. Handling Missing or Null Data
   Replace or update missing values in key columns to maintain data integrity.
*/

-- Replace NULL values in critical columns with a placeholder or calculated value
UPDATE PortfolioProject.dbo.NashvilleHousing
SET PropertyAddress = ISNULL(PropertyAddress, 'Unknown Address'),
    SaleAmount = ISNULL(SaleAmount, 0)  -- Assuming 0 is a logical placeholder for missing sales data
WHERE PropertyAddress IS NULL OR SaleAmount IS NULL;

-- Validate the updates
SELECT COUNT(*) AS NullValuesAfterUpdate
FROM PortfolioProject.dbo.NashvilleHousing
WHERE PropertyAddress = 'Unknown Address' OR SaleAmount = 0;

/*
4. Data Integrity Check
   Ensures there are no duplicate entries based on ParcelID and SaleDate.
*/

-- Identify potential duplicates
SELECT ParcelID, SaleDate, COUNT(*) AS RecordCount
FROM PortfolioProject.dbo.NashvilleHousing
GROUP BY ParcelID, SaleDate
HAVING COUNT(*) > 1;

-- Remove duplicates while keeping the most recent entry
WITH RankedRecords AS (
    SELECT *, 
           ROW_NUMBER() OVER (PARTITION BY ParcelID, SaleDate ORDER BY SaleDate DESC) AS rn
    FROM PortfolioProject.dbo.NashvilleHousing
)
DELETE FROM RankedRecords
WHERE rn > 1;

-- Verify no duplicates remain
SELECT ParcelID, SaleDate, COUNT(*) AS RecordCount
FROM PortfolioProject.dbo.NashvilleHousing
GROUP BY ParcelID, SaleDate
HAVING COUNT(*) > 1;

/*
5. Advanced Data Manipulation
   Additional queries to showcase advanced SQL techniques.
*/

-- Add a calculated column for the year of sale
ALTER TABLE PortfolioProject.dbo.NashvilleHousing
ADD SaleYear INT;

UPDATE PortfolioProject.dbo.NashvilleHousing
SET SaleYear = YEAR(SaleDate);

-- Validate the new column
SELECT DISTINCT SaleYear
FROM PortfolioProject.dbo.NashvilleHousing
ORDER BY SaleYear;

/* 
End of Data Cleaning Script
This script reflects a comprehensive understanding of data cleaning processes, ensuring data quality and reliability for analysis.
*/


/*
Data Analysis Portfolio Project Queries
Author: Kamryn Evensen

This SQL script is designed to analyze the 'NashvilleHousing' dataset after the data cleaning process. The queries demonstrate my ability to extract meaningful insights and perform data analysis using SQL.

*/

/* 
1. Summary Statistics 
   This section calculates key summary statistics for the dataset.
*/

-- Calculate the average, minimum, and maximum sale amount
SELECT 
    AVG(SaleAmount) AS AverageSaleAmount,
    MIN(SaleAmount) AS MinimumSaleAmount,
    MAX(SaleAmount) AS MaximumSaleAmount
FROM PortfolioProject.dbo.NashvilleHousing;

-- Count the number of properties sold each year
SELECT 
    SaleYear, 
    COUNT(*) AS NumberOfSales
FROM PortfolioProject.dbo.NashvilleHousing
GROUP BY SaleYear
ORDER BY SaleYear;

/*
2. Price Distribution Analysis
   Analyze the distribution of sale amounts to understand the spread and identify outliers.
*/

-- Calculate the sale amount distribution using quartiles
SELECT 
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY SaleAmount) AS Q1,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY SaleAmount) AS Median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY SaleAmount) AS Q3
FROM PortfolioProject.dbo.NashvilleHousing;

-- Identify potential outliers based on the IQR method
WITH Quartiles AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY SaleAmount) AS Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY SaleAmount) AS Q3
    FROM PortfolioProject.dbo.NashvilleHousing
)
SELECT *
FROM PortfolioProject.dbo.NashvilleHousing AS nh
CROSS JOIN Quartiles AS q
WHERE SaleAmount < (q.Q1 - 1.5 * (q.Q3 - q.Q1))
   OR SaleAmount > (q.Q3 + 1.5 * (q.Q3 - q.Q1));

/*
3. Geographic Analysis
   Analyze sales by location to identify trends based on property addresses or zip codes.
*/

-- Count the number of sales by zip code
SELECT 
    PropertyZipCode, 
    COUNT(*) AS NumberOfSales,
    AVG(SaleAmount) AS AverageSaleAmount
FROM PortfolioProject.dbo.NashvilleHousing
GROUP BY PropertyZipCode
ORDER BY NumberOfSales DESC;

-- Identify the top 5 most expensive neighborhoods by average sale amount
SELECT 
    PropertyAddress, 
    AVG(SaleAmount) AS AverageSaleAmount
FROM PortfolioProject.dbo.NashvilleHousing
GROUP BY PropertyAddress
ORDER BY AverageSaleAmount DESC
LIMIT 5;

/*
4. Time Series Analysis
   Analyze trends over time to understand how the housing market has evolved.
*/

-- Calculate monthly sales volume over the years
SELECT 
    YEAR(SaleDate) AS SaleYear, 
    MONTH(SaleDate) AS SaleMonth,
    COUNT(*) AS NumberOfSales,
    SUM(SaleAmount) AS TotalSalesAmount
FROM PortfolioProject.dbo.NashvilleHousing
GROUP BY YEAR(SaleDate), MONTH(SaleDate)
ORDER BY SaleYear, SaleMonth;

-- Calculate year-over-year growth in sales amount
SELECT 
    SaleYear, 
    SUM(SaleAmount) AS TotalSalesAmount,
    LAG(SUM(SaleAmount), 1) OVER (ORDER BY SaleYear) AS PreviousYearSales,
    (SUM(SaleAmount) - LAG(SUM(SaleAmount), 1) OVER (ORDER BY SaleYear)) / LAG(SUM(SaleAmount), 1) OVER (ORDER BY SaleYear) * 100 AS YoYGrowth
FROM PortfolioProject.dbo.NashvilleHousing
GROUP BY SaleYear
ORDER BY SaleYear;

/*
5. Correlation Analysis
   Analyze the relationship between different variables to identify correlations.
*/

-- Calculate the correlation between property size and sale amount
SELECT 
    ROUND(CORR(PropertySize, SaleAmount), 2) AS CorrelationCoefficient
FROM PortfolioProject.dbo.NashvilleHousing
WHERE PropertySize IS NOT NULL AND SaleAmount IS NOT NULL;

/* 
End of Data Analysis Script
This script demonstrates a comprehensive analysis of the Nashville housing data, highlighting key trends, distributions, and correlations.
*/
