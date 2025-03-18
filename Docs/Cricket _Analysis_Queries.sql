Cricket Match Data Analysis Queries

1. Top 10 batsmen by total runs in ODI matches
SELECT batsman, SUM(runs_batter) AS total_runs
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE matches.match_type = 'ODI'
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;

2. Leading wicket-takers in T20 matches
SELECT bowler, COUNT(*) AS total_wickets
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE matches.match_type = 'T20' AND runs_total = 0
GROUP BY bowler
ORDER BY total_wickets DESC
LIMIT 10;

3. Team with the highest win percentage in Test matches
SELECT team_name, COUNT(*) AS total_wins,
(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM matches WHERE match_type = 'Test')) AS win_percentage
FROM matches
WHERE result = team_name
GROUP BY team_name
ORDER BY win_percentage DESC
LIMIT 1;

4. Total number of centuries across all match types
SELECT match_type, COUNT(*) AS total_centuries
FROM (
    SELECT match_type, batter
    FROM deliveries
    JOIN matches ON deliveries.match_id = matches.match_id
    WHERE runs_batter >= 100
) AS centuries
GROUP BY match_type;

5. Matches with the narrowest margin of victory
SELECT match_id, team_name, result
FROM matches
WHERE result LIKE '%runs%'
ORDER BY CAST(SUBSTRING_INDEX(result, ' ', 1) AS UNSIGNED)
LIMIT 5;

6. Most sixes hit by a player in a single ODI match
SELECT batter, match_id, COUNT(*) AS total_sixes
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE matches.match_type = 'ODI' AND runs_batter = 6
GROUP BY batter, match_id
ORDER BY total_sixes DESC
LIMIT 1;

7. Fastest century in T20 matches
SELECT batter, match_id, MIN(over_number) AS fastest_century
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE matches.match_type = 'T20' AND runs_batter >= 100
GROUP BY batter, match_id
ORDER BY fastest_century ASC
LIMIT 1;

8. Highest individual score in Test matches
SELECT batter, match_id, MAX(runs_batter) AS highest_score
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE matches.match_type = 'Test'
GROUP BY batter, match_id
ORDER BY highest_score DESC
LIMIT 1;

9. Most five-wicket hauls in ODIs
SELECT bowler, COUNT(*) AS five_wicket_hauls
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE matches.match_type = 'ODI' AND runs_total = 0
GROUP BY bowler
ORDER BY five_wicket_hauls DESC
LIMIT 10;

10. Team with the most sixes in IPL history
SELECT team_name, COUNT(*) AS total_sixes
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE runs_batter = 6
GROUP BY team_name
ORDER BY total_sixes DESC
LIMIT 1;

11. Longest Test Matches (by Days)
SELECT match_id, city, season, DATEDIFF(MAX(season), MIN(season)) AS match_duration
FROM matches
WHERE match_type = 'Test'
GROUP BY match_id
ORDER BY match_duration DESC
LIMIT 5;

12. Number of Matches Won by Each Team in T20s
SELECT result AS team, COUNT(*) AS wins
FROM matches
WHERE match_type = 'T20'
GROUP BY team
ORDER BY wins DESC;

13. Most Successful Captain in ODIs
SELECT toss_winner AS captain, COUNT(*) AS matches_won
FROM matches
WHERE match_type = 'ODI' AND toss_decision = 'bat'
GROUP BY captain
ORDER BY matches_won DESC
LIMIT 5;

14. Top 5 Fastest Centuries in ODIs
SELECT batter, match_id, MIN(over_number) AS fastest_century
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE matches.match_type = 'ODI' AND runs_batter >= 100
GROUP BY batter, match_id
ORDER BY fastest_century ASC
LIMIT 5;

15. Number of Matches Played Per Year
SELECT YEAR(season) AS year, COUNT(*) AS total_matches
FROM matches
GROUP BY year
ORDER BY year DESC;
