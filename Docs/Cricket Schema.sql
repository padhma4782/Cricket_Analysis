Cricket Match Database Schema

Table for storing match details
CREATE TABLE matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    match_type ENUM('Test', 'ODI', 'T20'),
    match_number INT,
    city VARCHAR(100),
    venue VARCHAR(255),
    season VARCHAR(20),
    result VARCHAR(50),
    toss_winner VARCHAR(50),
    toss_decision VARCHAR(10)
);

Table for storing teams
CREATE TABLE teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    team_name VARCHAR(50),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

Table for storing players
CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    team_name VARCHAR(50),
    player_name VARCHAR(100),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

Table for storing umpires and match referees
CREATE TABLE officials (
    official_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    role VARCHAR(50),
    name VARCHAR(100),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

Table for storing innings details
CREATE TABLE innings (
    innings_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    team VARCHAR(50),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

Table for storing ball-by-ball deliveries
CREATE TABLE deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    innings_id INT,
    over_number INT,
    batter VARCHAR(100),
    bowler VARCHAR(100),
    non_striker VARCHAR(100),
    runs_batter INT,
    runs_extras INT,
    runs_total INT,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (innings_id) REFERENCES innings(innings_id)
);

Table for storing wicket details
CREATE TABLE wickets (
    wicket_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    delivery_id INT,
    player_out VARCHAR(100),
    kind VARCHAR(50),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id)
);
