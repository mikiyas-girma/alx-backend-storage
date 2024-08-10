-- SQL script that creates a stored procedure AddBonus
-- that adds a new correction for a student.

DELIMITER //

CREATE PROCUDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score FLOAT
)
BEGIN
    IF NOT EXISTS  (SELECT name FROM projects WHERE name=project_name) THEN
        INSERT INTO projects (name) VALUES (project_name);
    END IF;

    DECLARE project_id INT;

    SELECT id INTO project_id
    FROM projects 
    WHERE name=project_name;

    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
END //

DELIMITER ;
