tournament - A module for running a swiss tournement. Includes support for byes
and dropping players.

use tournament.registerPlayer to sign players up for a tournament.

tournament.swissPairings generates pairings, the results of which should be
reported via the tournament.reportMatch method, inputting the winner first, 
then loser.

If a player drops from a tournement, use the tournament.dropPlayer method with
the player's id number as the argument to remove them from future pairings.