CREATE DATABASE benchmark_microservicios;
USE benchmark_microservicios;

CREATE TABLE benchmark_records (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    test_id VARCHAR(100) NOT NULL,
    request_id VARCHAR(100) NOT NULL,
    value INT NOT NULL,
    description TEXT,
    sent_at DATETIME,
    service_instance VARCHAR(100) NOT NULL,
    db_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_benchmark_request UNIQUE (test_id, request_id)
);


DROP PROCEDURE IF EXISTS insert_benchmark_record;

DELIMITER $$

CREATE PROCEDURE insert_benchmark_record(
    IN p_test_id VARCHAR(100),
    IN p_request_id VARCHAR(100),
    IN p_value INT,
    IN p_description TEXT,
    IN p_sent_at DATETIME,
    IN p_service_instance VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO benchmark_records (
        test_id,
        request_id,
        value,
        description,
        sent_at,
        service_instance
    )
    VALUES (
        p_test_id,
        p_request_id,
        p_value,
        p_description,
        p_sent_at,
        p_service_instance
    );

    COMMIT;
END $$

DELIMITER ;

CALL insert_benchmark_record(
    'benchmark-api1-1000-c10-001',
    'REQ-000001',
    1,
    'registro de prueba',
    '2026-05-26 14:30:10',
    'api-1'
);

SELECT * FROM benchmark_records;

SELECT
    request_id,
    service_instance,
    db_created_at
FROM benchmark_records
ORDER BY id DESC
LIMIT 10;



SELECT
    service_instance,
    COUNT(*) AS total
FROM benchmark_records
GROUP BY service_instance
ORDER BY service_instance;



SELECT COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-1000-c10-001';

SELECT
    service_instance,
    COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-1000-c10-001'
GROUP BY service_instance
ORDER BY service_instance;

SELECT COUNT(*)
FROM benchmark_records
WHERE test_id = 'benchmark-api4-1000-c10-001';


SELECT COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-20-c5-002';

SELECT
    service_instance,
    COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-20-c5-002'
GROUP BY service_instance;



SELECT COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-100-c10-003';

SELECT
    service_instance,
    COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-100-c10-003'
GROUP BY service_instance;


SELECT COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-1000-c100-004';

SELECT
    service_instance,
    COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-1000-c100-004'
GROUP BY service_instance;


SELECT COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-5000-c1000-005';

SELECT
    service_instance,
    COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-5000-c1000-005'
GROUP BY service_instance;


SELECT COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-10000-c10000-006';

SELECT
    service_instance,
    COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-10000-c10000-006'
GROUP BY service_instance;


SELECT COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'TU_TEST_ID';

SELECT test_id, COUNT(*) AS total
FROM benchmark_records
GROUP BY test_id
ORDER BY test_id;

SELECT COUNT(*) AS total_insertados
FROM benchmark_records
WHERE test_id = 'benchmark-api4-10000-c10000-006';