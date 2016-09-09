-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP TABLE IF EXISTS records;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

CREATE TABLE players (id serial primary key,
                      name text);
--currently mostly unused - facilitates future implementation of draws and
--eliminating rematches in the bracket.
CREATE TABLE matches (match serial primary key,
                      winner int references players(id),
                      loser int,
                      draw boolean);

CREATE TABLE records (id int primary key references players(id),
                      wins int,
                      matches int);
