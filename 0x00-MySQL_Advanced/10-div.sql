-- SQL script that creates a function SafeDiv that divides (and returns) the first by the second number or
-- returns 0 if the second number is equal to 0.

DELIMITER //

CREATE FUNCTION SafeDiv(
    a INT,
    b INT
)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    DECLARE res FLOAT;
    IF b = 0 THEN
        RETURN 0;
    ENDIF;
    SET res = CAST( a / b AS FLOAT);
    RETURN res;
END //

DELIMITER ;
