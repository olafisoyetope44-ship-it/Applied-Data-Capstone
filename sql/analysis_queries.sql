-- SpaceX Falcon 9 launch analysis queries
-- Dialect: SQLite
-- Before running: import dataset_part_2.csv into a table named launches.
-- Class = 1 means successful first-stage landing; Class = 0 means unsuccessful.
-- Rates below describe this historical dataset and are not causal or operational forecasts.

-- 1. Launch volume and recorded landing success by launch site
SELECT
    LaunchSite,
    COUNT(*) AS total_launches,
    SUM(Class) AS successful_landings,
    ROUND(100.0 * AVG(Class), 1) AS landing_success_pct
FROM launches
GROUP BY LaunchSite
ORDER BY landing_success_pct DESC;

-- 2. Landing success by orbit
SELECT
    Orbit,
    COUNT(*) AS total_launches,
    ROUND(100.0 * AVG(Class), 1) AS landing_success_pct
FROM launches
GROUP BY Orbit
HAVING COUNT(*) >= 3
ORDER BY landing_success_pct DESC;

-- 3. Year-over-year landing success trend
SELECT
    STRFTIME('%Y', Date) AS launch_year,
    COUNT(*) AS total_launches,
    ROUND(100.0 * AVG(Class), 1) AS landing_success_pct
FROM launches
WHERE Date IS NOT NULL
GROUP BY STRFTIME('%Y', Date)
ORDER BY launch_year;

-- 4. Compare average payload mass by landing outcome
SELECT
    CASE Class
        WHEN 1 THEN 'Successful landing'
        WHEN 0 THEN 'Unsuccessful landing'
        ELSE 'Unknown'
    END AS landing_outcome,
    COUNT(*) AS total_launches,
    ROUND(AVG(PayloadMass), 1) AS avg_payload_kg,
    ROUND(MIN(PayloadMass), 1) AS min_payload_kg,
    ROUND(MAX(PayloadMass), 1) AS max_payload_kg
FROM launches
WHERE PayloadMass IS NOT NULL
GROUP BY Class
ORDER BY Class DESC;

-- 5. Landing success by booster flight count
SELECT
    Flights AS booster_flight_number,
    COUNT(*) AS total_launches,
    ROUND(100.0 * AVG(Class), 1) AS landing_success_pct
FROM launches
GROUP BY Flights
ORDER BY Flights;

-- 6. Overall dataset quality check
SELECT
    COUNT(*) AS row_count,
    SUM(CASE WHEN Date IS NULL OR TRIM(Date) = '' THEN 1 ELSE 0 END) AS missing_dates,
    SUM(CASE WHEN LaunchSite IS NULL OR TRIM(LaunchSite) = '' THEN 1 ELSE 0 END) AS missing_launch_sites,
    SUM(CASE WHEN PayloadMass IS NULL THEN 1 ELSE 0 END) AS missing_payload_mass,
    SUM(CASE WHEN Class IS NULL THEN 1 ELSE 0 END) AS missing_landing_class
FROM launches;
