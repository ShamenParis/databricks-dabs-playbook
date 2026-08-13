-- 1. Insert new records using raw SQL
INSERT INTO main.demo.sql_lesson_data (id, status, processed_date)
VALUES 
    (1, 'SUCCESS', current_timestamp()),
    (2, 'SUCCESS', current_timestamp()),
    (3, 'FAILED', current_timestamp());

-- COMMAND ----------
-- 2. Select the data to output it in the Workflows UI logs
SELECT 
    status, 
    COUNT(id) as record_count 
FROM main.demo.sql_lesson_data
GROUP BY status;