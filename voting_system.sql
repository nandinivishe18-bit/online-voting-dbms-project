CREATE DATABASE voting_system;

USE voting_system;


-- Voters Table

CREATE TABLE voters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    prn VARCHAR(20) UNIQUE,
    email VARCHAR(100),
    mobile VARCHAR(15),
    age INT,
    password VARCHAR(255),
    voted_status INT DEFAULT 0
);


-- Candidates Table

CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    party VARCHAR(100),
    votes INT DEFAULT 0
);


-- Feedback Table

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100),
    q1_rating INT,
    q2_ease_of_use VARCHAR(10),
    q3_recommend VARCHAR(10)
);


-- Custom Function

DELIMITER //

CREATE FUNCTION FormatCandidateName(
    c_name VARCHAR(100),
    c_party VARCHAR(100)
)
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN

    RETURN CONCAT(
        UPPER(c_name),
        ' - Member of ',
        c_party
    );

END //

DELIMITER ;


-- Database View

CREATE VIEW election_results_summary AS

SELECT
    name AS Candidate_Name,
    party AS Political_Party,
    votes AS Total_Votes

FROM candidates

ORDER BY votes DESC;


-- Database Trigger

DELIMITER //

CREATE TRIGGER before_voter_insert

BEFORE INSERT ON voters

FOR EACH ROW

BEGIN

    SET NEW.name =
        CONCAT(
            UPPER(LEFT(NEW.name, 1)),
            LOWER(SUBSTRING(NEW.name, 2))
        );

END //

DELIMITER ;


-- Initial Candidate Data

INSERT INTO candidates
(name, party, votes)
VALUES
('Shruti Rao', 'Technical Secretary', 0),
('Priya Patil', 'Innovation Party', 0),
('Rahul Verma', 'Student Alliance', 0);
