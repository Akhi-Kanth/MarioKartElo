import pandas as pd

class MarioKartEloSystem:
    def __init__(self, *args):
        # Step 1: Read player data from CSV file
        self.all_player_data = pd.read_csv("player_data.csv")

        # Step 2: Extract information for specified players
        self.player_info = [name for name in args]

        # Step 3: Calculate initial Elo ratings for specified players
        self.player_info = [[name, self.all_player_data[name][0]] for name in self.player_info] 
        self.number_of_players = len(self.player_info)

        # Step 4: Set up constants for adjusting Elo rating changes 
        self.K_CONSTANT = 1  # Can be adjusted to control the magnitude of Elo rating changes 
        self.L_CONSTANT = 1  # Can be adjusted to control the influence of the difference in Elo ratings 

        # Step 5: Set up base Elo rating for new players
        self.BOT_ELO = 2000 / 3  # Base Elo rating for new players (assumed to be the average Elo rating in the system)

    def new_elo(self):
        # Calculate the Elo rating of the bot based on the number of players in the game.
        bot_elo = self.BOT_ELO * (12 - self.number_of_players)

        # Calculate the Elo rating sum of other players excluding the specified player.
        other_players_elo = sum([player[2] for player in self.player_info if player[0] is not self.player_info[index][0]])

        # Compute the exponent for the Elo rating difference between other players and the bot.
        exponent = ((((other_players_elo + bot_elo) / 11) - self.player_info[index][1]) / 400)

        # Calculate the expected outcome based on Elo rating differences.
        expected_outcome = 1 / (1 + pow(10, exponent))

        # Convert the expected outcome to a win rate percentage and round it to two decimal places.
        return round(expected_outcome * 100, 2) 
                    

    def points_incorp(self, index):
        # Step 1: Get the player inputed points
        player_points = self.player_info[index][3]

        # Step 2: Get the total points of all the players
        total_player_points = sum([player[3] for player in self.player_info])

        # Step 3: Return the quotient multiplied by the L constant
        return (self.L_CONSTANT * (player_points / total_player_points))

    def actual_outcome(self, index):
        return self.player_info[index][2]


    def add_players(self, *args):    
        # Loop through each player object provided in the arguments.
        for player in args:
            # Insert each player at the beginning of the player data list with an initial score of 1000.
            self.all_player_data.insert(0, player, 1000, allow_duplicates=False)

        # Print the updated player data list.
        print(self.all_player_data)

        # Save the updated player data to a CSV file named "player_data.csv" without indexing.
        self.all_player_data.to_csv("player_data.csv", index=False) 


    def update_csv(self):
        # Iterate through each player in the game.
        for player in self.player_info:
            # Check if the player exists in the player data DataFrame.
            if player[0] in self.all_player_data.columns:
                # If the player exists, update their information in the DataFrame.
                self.all_player_data.loc[0, player[0]] = round(player[4], 2)

        # Save the updated player data to a CSV file named "player_data.csv" without indexing.
        self.all_player_data.to_csv("player_data.csv", index=False)

