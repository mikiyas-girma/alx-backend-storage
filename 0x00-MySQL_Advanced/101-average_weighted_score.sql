-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users U, 
    (SELECT U.id, SUM(score * weight) / SUM(weight) AS weighted_avg 
    FROM users U 
    JOIN corrections C ON U.id=C.user_id 
    JOIN projects  P ON C.project_id=P.id 
    GROUP BY U.id)
  AS WA
  SET U.average_score = WA.weighted_avg 
  WHERE U.id=WA.id;
END; //

DELIMITER ;
