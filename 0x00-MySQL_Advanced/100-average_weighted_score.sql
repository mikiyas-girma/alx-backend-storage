-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE weighted_score_sum FLOAT DEFAULT 0;
    DECLARE average_weighted_score FLOAT DEFAULT 0;
    
    -- Calculate the sum of weights
    SELECT SUM(p.weight) 
    INTO total_weight
    FROM corrections c
    INNER JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- Calculate the sum of weighted scores
    SELECT SUM(c.score * p.weight)
    INTO weighted_score_sum
    FROM corrections c
    INNER JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- If total_weight is not 0, calculate the average weighted score
    IF total_weight > 0 THEN
        SET average_weighted_score = weighted_score_sum / total_weight;
    ELSE
        SET average_weighted_score = 0;
    END IF;
    
    -- Update the user's average_score
    UPDATE users
    SET average_score = average_weighted_score
    WHERE id = user_id;
    
END //

DELIMITER ;
