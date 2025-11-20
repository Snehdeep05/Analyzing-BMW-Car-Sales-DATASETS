CREATE TABLE BMW (
    Model VARCHAR(50),
    Year INT,
    Region VARCHAR(50),
    Color VARCHAR(20),
    Fuel_Type VARCHAR(20),
    Transmission VARCHAR(20),
    Engine_Size_L DECIMAL(3,1),
    Mileage_KM INT,
    Price_USD DECIMAL(10,2),
    Sales_Volume INT,
    Sales_Classification VARCHAR(10)
);
copy BMW FROM 'E:\SQL\sql-ultimate-course\datas' DELIMITER ',' CSV HEADER;
SELECT * FROM BMW; 


-- Insight 1: Overall sales volume by model (top sellers)
SELECT Model, 
       SUM(Sales_Volume) as Total_Sales
FROM BMW
GROUP BY Model
ORDER BY Total_Sales DESC;


-- Insight 2: Sales trend by year
SELECT Year, 
       SUM(Sales_Volume) as Annual_Sales, 
       AVG(Price_USD) as Avg_Price
FROM BMW
GROUP BY Year
ORDER BY Year;

-- Insight 3: Regional sales distribution
SELECT Region, SUM(Sales_Volume) as Regional_Sales,
       ROUND(SUM(Sales_Volume) * 100.0 / (SELECT SUM(Sales_Volume) FROM BMW), 2) as Percentage
FROM BMW
GROUP BY Region
ORDER BY Regional_Sales DESC;


-- Insight 4: Most popular colors globally
SELECT Color, COUNT(*) as Count, 
       SUM(Sales_Volume) as Total_Sales
FROM BMW
GROUP BY Color
ORDER BY Total_Sales DESC;


-- Insight 5: Fuel type preference by region
SELECT Region, Fuel_Type, SUM(Sales_Volume) as Sales
FROM BMW
GROUP BY Region, Fuel_Type
ORDER BY Region, Sales DESC;

-- Insight 6: Transmission preference trend
SELECT Year, Transmission, COUNT(*) as Count,
       AVG(Price_USD) as Avg_Price
FROM BMW
GROUP BY Year, Transmission
ORDER BY Year, Count DESC;

-- Insight 7: Engine size trends over years
SELECT Year, AVG(Engine_Size_L) as Avg_Engine_Size,
       MIN(Engine_Size_L) as Min_Engine_Size,
       MAX(Engine_Size_L) as Max_Engine_Size
FROM BMW
GROUP BY Year
ORDER BY Year;


-- Insight 8: Price analysis by model and fuel type
SELECT Model, Fuel_Type, 
       AVG(Price_USD) as Avg_Price,
       AVG(Mileage_KM) as Avg_Mileage
FROM BMW
GROUP BY Model, Fuel_Type
ORDER BY Avg_Price DESC;

-- Insight 9: High vs Low sales classification analysis
SELECT Sales_Classification, 
       COUNT(*) as Count,
       AVG(Price_USD) as Avg_Price,
       AVG(Sales_Volume) as Avg_Sales_Volume
FROM BMW
GROUP BY Sales_Classification;

-- Insight 10: Regional price variations
SELECT Region, 
       AVG(Price_USD) as Avg_Price,
       MIN(Price_USD) as Min_Price,
       MAX(Price_USD) as Max_Price
FROM BMW
GROUP BY Region
ORDER BY Avg_Price DESC;


-- Insight 11: Electric vehicle adoption by year and region
SELECT Year, Region, COUNT(*) as EV_Count,
       SUM(Sales_Volume) as EV_Sales
FROM BMW
WHERE Fuel_Type = 'Electric'
GROUP BY Year, Region
ORDER BY Year, EV_Sales DESC;

-- Insight 12: Mileage impact on price
SELECT 
    CASE 
        WHEN Mileage_KM < 50000 THEN 'Low Mileage (<50k)'
        WHEN Mileage_KM BETWEEN 50000 AND 100000 THEN 'Medium Mileage (50k-100k)'
        ELSE 'High Mileage (>100k)'
    END as Mileage_Category,
    AVG(Price_USD) as Avg_Price,
    COUNT(*) as Count
FROM BMW
GROUP BY Mileage_Category
ORDER BY Avg_Price DESC;

-- Insight 13: Most profitable models (high price, high sales)
SELECT Model, 
       AVG(Price_USD) as Avg_Price,
       SUM(Sales_Volume) as Total_Sales,
       (AVG(Price_USD) * SUM(Sales_Volume)) as Revenue_Estimate
FROM BMW
GROUP BY Model
ORDER BY Revenue_Estimate DESC
LIMIT 10;

-- Insight 14: Seasonal/Yearly trends in specific models
SELECT Year, Model, SUM(Sales_Volume) as Sales
FROM BMW
WHERE Model IN ('5 Series', '3 Series', 'X5', 'X3')
GROUP BY Year, Model
ORDER BY Model, Year;

-- Insight 15: Color preferences by region
SELECT Region, Color, COUNT(*) as Count
FROM BMW
GROUP BY Region, Color
ORDER BY Region, Count DESC;

-- Insight 16: Fuel type evolution over years
SELECT Year, Fuel_Type, COUNT(*) as Count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Year), 2) as Percentage
FROM BMW
GROUP BY Year, Fuel_Type
ORDER BY Year, Count DESC;

-- Insight 17: Transmission type correlation with engine size
SELECT Transmission, 
       AVG(Engine_Size_L) as Avg_Engine_Size,
       AVG(Price_USD) as Avg_Price
FROM BMW
GROUP BY Transmission;

-- Insight 18: Regional preferences for specific models
SELECT Region, Model, SUM(Sales_Volume) as Sales
FROM BMW
GROUP BY Region, Model
ORDER BY Sales DESC
LIMIT 15;

-- Insight 19: Price segmentation analysis
SELECT 
    CASE 
        WHEN Price_USD < 50000 THEN 'Budget (<50k)'
        WHEN Price_USD BETWEEN 50000 AND 80000 THEN 'Mid-Range (50k-80k)'
        WHEN Price_USD BETWEEN 80000 AND 120000 THEN 'Premium (80k-120k)'
        ELSE 'Luxury (>120k)'
    END as Price_Segment,
    COUNT(*) as Count,
    AVG(Sales_Volume) as Avg_Sales_Volume
FROM BMW
GROUP BY Price_Segment
ORDER BY Count DESC;

-- Insight 20: Model-year combination performance
SELECT Model, Year, 
       AVG(Price_USD) as Avg_Price,
       SUM(Sales_Volume) as Total_Sales
FROM BMW
GROUP BY Model, Year
ORDER BY Total_Sales DESC
LIMIT 15;


-- Insight 21 Total Sales Volume and Revenue by Region
SELECT 
    Region,
    COUNT(*) as Number_of_Transactions,
    SUM(Sales_Volume) as Total_Cars_Sold,
    ROUND(AVG(Price_USD),2) as Average_Price,
    MIN(Price_USD) as Min_Price,
    MAX(Price_USD) as Max_Price
FROM BMW
GROUP BY Region
ORDER BY Total_Cars_Sold DESC;


-- Insight 22 Year-over-Year Trends
SELECT 
    Year,
	model,
    Round(AVG(Price_USD),2) as Avg_Price,
    SUM(Sales_Volume) as Total_Sales_Volume
FROM BMW
GROUP BY Year,model
ORDER BY Year,model;


-- Insight 23 Sales Classification by Model
SELECT 
    Region,
    Model,
	Sales_Classification,
    COUNT(*) as Count
FROM BMW
GROUP BY Model,Region,Sales_Classification
ORDER BY Model,Region, Sales_Classification;


-- Insight 24 Most Popular Model By Region

SELECT 
    Region, 
    Model,
    COUNT(*) as Number_of_Transactions,
    RANK() OVER (PARTITION BY Region ORDER BY COUNT(*) DESC) as Model_Rank_In_Region
FROM BMW
GROUP BY Region, Model
ORDER BY Region, Number_of_Transactions DESC;

-- Insight 25 Most Lucrative Regions
SELECT 
    Year,
    Region,
    SUM(Price_USD * Sales_Volume) as Estimated_Revenue,
    RANK() OVER (PARTITION BY Year ORDER BY SUM(Price_USD * Sales_Volume) DESC) as Revenue_Rank_Per_Year
FROM BMW
GROUP BY Year, Region
ORDER BY Year, Estimated_Revenue DESC;


--  Insight 26  Highest Priced Engine Size per Model
SELECT 
    Model,
    Engine_Size_L,
    MAX(Price_USD) as Max_Price,
    DENSE_RANK() OVER (PARTITION BY Model ORDER BY MAX(Price_USD) DESC) as Price_Rank_Per_Model
FROM BMW
GROUP BY Model, Engine_Size_L
ORDER BY Model, Max_Price DESC;

-- Insight 27 Ranking higest sales by region 
SELECT 
       REGION,
	   FUEL_TYPE,
	   MAX(SALES_VOLUME) AS HIGEST_SALES,
	   DENSE_RANK()OVER(PARTITION BY region ORDER BY MAX(SALES_VOLUME) desc) as ranking_by_region
FROM BMW
GROUP BY REGION, FUEL_TYPE;
	   

-- Insight 28 Ranking higest sales by year

SELECT year,
	   FUEL_TYPE,
	   MAX(SALES_VOLUME) AS HIGEST_SALES,
       DENSE_RANK() OVER(PARTITION BY year ORDER BY MAX(SALES_VOLUME) desc) as ranking_by_year
FROM BMW
GROUP BY year, FUEL_TYPE;

