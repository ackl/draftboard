# Use Case Definition
A list of use cases for the application. One actor, the user, is defined for these use cases. The application use cases can be divided into three modules:

* Player
* Game
* Tournament

### Player Module
Handles creating, retrieving, updating, and deleting Player model objects. Also responsible for retrieving Game and Tournament objects related to an instance of Player.

* Store information for a player, including name and life total.
* Create a new player by providing a name for that player; life total should default to 20.
* Retrieve a list of all players; should be sorted by performance.
* Retrieve data on a single player, data includes game performance, tournament participation, current life total, and name.
* Update a player's information, name and life total.
* Delete a player, user should be prompted before deletion.
* Retrieve a list of all games a player was involved in.
* Retrieve a list of all tournaments a player has participated in.
* Retrieve game information for a player's ongoing game, if any.


### Game Module
Handles creating, retrieving, updating, and deleting Game model objects. Has collection of Player objects and shares the responsibility of changing life totals.

* Store information for a game, including involved players, wins for each, best of number, and format.
* Determine whether a game is ongoing or not based on number of wins for a player, and the current best of number (wins/2 > best_of == completed).
* Create a new game by providing 2 or more players, best of number, and format; if a specified player is already involved in an ongoing game return an error linking to that game for resolution. This game should not be associated with any tournament.
* Retrieve a list of all games, sorted by creation date. Ongoing games should be highlighted and pushed to the top.
* Retrieve a list of all ongoing games, if any.
* Retrieve data on a single game; data includes all players involved and number of wins for each, the format, the best of number, and whether the game is ongoing or not. If not, victor should be indicated.
* Update a game, updates include changing participants, participant life totals, best of number, format, and number of wins for a participant. Updating a win for a player should reset all involved player life totals to 20.
* Delete a game, user should be prompted before deletion.


## Tournament Module
Handles creating, retrieving, updating, and deleting Tournament model objects. Stores a collection of aggregate Game and Player objects.

* Store information for a tournament, including name, involved players, completed and ongoing games, and format.
* Determine whether a tournament is ongoing or not based on list of games that are complete and player list. All tournaments are round-robin.
* Create a new tournament by providing a name and format. Collection of Game and Player objects can remain empty at this stage.
* Add a player as a participant to the tournament, choose from list of existing players or add a new player.
* Create a game instance for a tournament by providing 2 players chosen from the participants list and best of number. Format is automatically set as the tournament's format and the game object reference added to the collection.
* Retrieve a list of tournaments, sorted by creation date. Ongoing tournaments should be highlighted and pushed to the top.
* Retrieve a list of ongoing tournaments, if any.
* Retrieve data on a single tournament; data includes points leaderboard, games list, name, and format. If the tournament is ongoing, participants in an ongoing game should be paired together with a link to that game's page, if complete the victor indicated.
* Update a tournament, updates include changing name and format, and adding games and participants. Life totals should not be changed from this module, only individual Game and Player pages should have this function.
* Delete a tournament, user should be prompted before deletion. Deleting a tournament should delete all games in that tournament's collection.

