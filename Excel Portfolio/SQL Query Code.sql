-- to calcculate the total ssles and total profit

SELECT 
	SUM(sales_amount) AS total_sales
FROM 
	sales;



-- to calculate total sales, total profit and profit marin percentage for each product category
   
SELECT 
	product_category,
	SUM(sales_amount) AS total_sales,
	SUM(profit_amount) as total_profit,
	(SUM(profit_amount) / SUM(sales_amount)) * 100 AS profit_margin_percentage
FROM
	sales
GROUP BY
	product_category;

-- to calculate the total units sold for each product

SELECT
	product_name,
    SUM(units_sold) as units_sold
FROM
	sales
GROUP BY
	product_name
ORDER BY
	units_sold DESC;

-- Quesry to calculate the percentage of total sales for each region

-- subquery to calculate total sales for each region

WITH RegionalSales AS (
	SELECT
		region,
        SUM(sales_amount) AS total_sales
	FROM
		sales
	GROUP BY
		region
).

-- subquesry to calculate the overall total sales
TotalSales AS (
	SELECT
		SUM(sales_amount) AS Total_Sales
	FROM
		sales
)

-- Main Qquery to calculate the percentage sales by region
SELECT 
	r.region,
    r.total_sales,
    (r.total_sales / t.total_sales) * 100 AS percentage_sales
FROM
	RegionalSales r,
    TotalSales t;


-- query to calculate sales growth by quarter

SELECT
	DATE_FORMAT(sales_date, '%Y-Q%q') AS Qauarter,
    SUM(sales_amount) AS total_sales,
    SUM(profit_amount) AS total_profit
FROM
	sales
GROUP BY
	DATE_FORMAT(sales_date, '%Y-Q%q')
ORDER BY 
	Quarter;



