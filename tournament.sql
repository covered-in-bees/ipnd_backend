-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (id serial primary key,
                      name text);
--the serial is currently mostly unused - facilitates future implementation of
--draws and eliminating rematches in the bracket.
CREATE TABLE matches (match serial primary key,
                      winner int references players(id),
                      loser int,
                      draw boolean);

CREATE VIEW wincount AS
                    SELECT players.id, coalesce(count(matches.winner),0) as wins
                    FROM players
                    LEFT JOIN matches ON matches.winner = players.id
                    GROUP BY players.id;
                    
CREATE VIEW losscount AS
                    SELECT players.id, coalesce(count(matches.loser),0) as losses
                    FROM players
                    LEFT JOIN matches ON matches.loser = players.id
                    GROUP BY players.id;
