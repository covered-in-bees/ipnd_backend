<h1>tournament</h1>
<h2>A module with tools for running a [Swiss tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament).</h2>

<h3>setup</h3>
Run the application by navigating to the container folder and initiate the database schema via:
`psql - f tournament.sql` 
Execute the test with the command: 
`python tournament_test.py`

<h3>usage</h3>
Use the `registerPlayer` method to sign players up for your tournament using the syntax:
```tournament.registerPlayer('<player's name>')```
This will automatically generate a unique id for the player.

`swissPairings` generates pairings.
The results should be reported via the `reportMatch` method, with the syntax:
```tournament.reportMatch(<winner's id>,<loser's id>)```
Note that any byes are automatically reported.

If a player drops from a tournement, use the `dropPlayer` method using the syntax:
```tournament.dropPlayer(<player's id>)```

`deleteMatches` deletes all match records, and thus resets the standings.
`deletePlayers` will delete all players and their matches from the database.

development progress:
- [x] byes supported
- [x] player dropping supported
- [ ] draws supported
- [ ] eliminate rematches in pairings