import pandas as pd

class MarioKartEloSystem:
    """
    A class representing an Elo rating system for Mario Kart players.

    Attributes:
        player_info (list): List containing player names and their corresponding Elo ratings.
        number_of_players (int): Total number of players in the system.
        K_CONSTANT (int): Constant used for adjusting the magnitude of Elo rating changes.
        L_CONSTANT (int): Constant used for adjusting the influence of the difference in Elo ratings.
        BOT_ELO (float): Base Elo rating for new players (assumed to be the average Elo rating in the system).

    Description:
        The MarioKartEloSystem class implements an Elo rating system to calculate the relative skill levels of players
        in a Mario Kart multiplayer racing game. It allows for the initialization of player data, updating player statistics,
        and calculating new Elo ratings after matches.

        The class provides the following functionality:

        - Initialization: Reads player data from a CSV file containing historical Elo ratings, extracts information for
          specified players, and sets up initial parameters for the Elo system.
        - New Elo Calculation: Calculates the new Elo rating for a given player after a match based on the outcome of the
          match and the player's performance.
        - Player Statistics Update: Updates the statistics (round rank and round points) for each player based on user input.
        - Expected Outcome Calculation: Calculates the expected outcome of a match for a given player based on the Elo
          ratings of all players.
        - Points Incorporation Calculation: Calculates the points to be incorporated into a player's Elo rating based on
          their performance in the match.
        - Actual Outcome Calculation: Placeholder method for calculating the actual outcome of a match (not implemented).

        All the player information is inputed into a list nested list:

        - Index 0: This refers to the name of the player
        - Index 1: This refers to the unupdated elo before the stats for this game get incorperated into the elo
        - Index 2: This refers to the rank (1 - 12) of the player that he got in the race that is being inputed
        - Index 3: This is points that the player got this round of races
        - Index 4: This the new elo that is being calculated and writen to the csv

    Usage:
        Initialize the MarioKartEloSystem with player names:
        >>> MKS = MarioKartEloSystem('akhil', 'nav', 'peter', 'rishi')

        Update player statistics:
        >>> MKS.update_player_stats()

        Calculate the expected outcome for a player:
        >>> MKS.expected_outcome('akhil')
    """

    def __init__(self, *args):
        """
        Initialize the MarioKartEloSystem class.

        Args:
            *args: Variable-length argument list containing player names.

        Attributes:
            player_info (list): List containing player names and their corresponding Elo ratings. 
            number_of_players (int): Total number of players in the system. 
            K_CONSTANT (int): Constant used for adjusting the magnitude of Elo rating changes. 
            L_CONSTANT (int): Constant used for adjusting the influence of the difference in Elo ratings. 
            BOT_ELO (float): Base Elo rating for new players (assumed to be the average Elo rating in the system). 

        Description:
            This method initializes the MarioKartEloSystem class by reading player data from a CSV file,
            extracting information for the specified players, and setting up initial parameters for the Elo system.
            The Elo system is a method for calculating the relative skill levels of players in two-player games.
            Here, it is adapted for Mario Kart, a multiplayer racing game.

            The method performs the following steps:
            1. Reads player data from a CSV file containing historical Elo ratings for all players.
            2. Extracts information for the specified players provided as arguments.
            3. Calculates the initial Elo ratings for the specified players.
            4. Sets up constants used for adjusting Elo rating changes (K_CONSTANT and L_CONSTANT).
            5. Sets up the base Elo rating for new players (BOT_ELO), assumed to be the average Elo rating in the system.
        """
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
        """
        Calculate the new Elo rating for each player after a match.

        Description:
            This method calculates the new Elo rating for each player after a match.
            It utilizes the Elo rating system formula, which considers each player's old Elo rating,
            the outcome of the match, and the points gained or lost based on each player's performance.

            The method performs the following steps:
            1. Iterates through each player in the player_info list.
            2. Retrieves the player's old Elo rating.
            3. Calculates the first part of the Elo rating change formula, representing the impact
               of the match outcome compared to the expected outcome.
            4. Calculates the second part of the Elo rating change formula, representing additional
               points gained or lost based on the player's in-game performance.
            5. Combines the two parts to calculate the new Elo rating for the player.
            6. Appends the new Elo rating to the player's existing data in the player_info list.

            Note: The Elo ratings are updated in-place within the player_info list.

        """

        # Iterate through each player in player_info
        for index, playerList in enumerate(self.player_info):
            # Step 1: Retrieve the player's old Elo rating
            old_elo = self.player_info[index][1]

            # Step 2: Calculate the first part of the Elo rating change formula
            part_one = (self.K_CONSTANT * (self.actual_outcome(index) - self.expected_outcome(index)))

            # Step 3: Calculate the second part of the Elo rating change formula
            part_two = self.points_incorp(index)

            # Step 4: Combine the two parts to calculate the new Elo rating for the player
            new_elo = old_elo + part_one + part_two

            # Step 5: Append the new Elo rating to the player's existing data in the player_info list
            self.player_info[index].append(new_elo)


    def update_player_stats(self):
        """
        Update the statistics (round rank and round points) for each player.

        Description:
            This method iterates through each player in the player_info list and prompts the user
            to input the round rank and round points for that player. It then appends this information
            to the player's existing data.

            The method handles invalid input by catching ValueError exceptions and prompting the user
            to enter valid integers for round rank and valid floats for round points.3
        """
        # Iterate through each player in player_info
        for index, player in enumerate(self.player_info):
            try:
                # Prompt user to input round rank and round points for the player
                round_rank = int(input(f"Enter round rank for player {player[0]}: "))
                round_points = float(input(f"Enter round points for player {player[0]}: "))
                
                # Append round rank and round points to the player's existing data
                self.player_info[index].append(round_rank)
                self.player_info[index].append(round_points)
                print()

            except ValueError:
                # Handle invalid input by prompting the user to enter valid integers for round rank
                # and valid floats for round points
                print("Invalid input. Please enter a valid integer for round rank and a valid float for round points.")
                


    def expected_outcome(self, index):
        """
        Calculate the expected win rate for a player in a game scenario.

        Args:
            player: The player for whom the win rate is to be calculated.

        Returns:
            float: The expected win rate of the player in percentage.

        Comments:
            - Calculate the Elo rating of the bot based on the number of players in the game.
            - Calculate the Elo rating of other players excluding the specified player.
            - Compute the exponent for the Elo rating difference between other players and the bot.
            - Calculate the expected outcome based on Elo rating differences.
            - Convert the expected outcome to a win rate percentage and round it to two decimal places.
        """

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
        """
        This method calculates the incorporation of points for a player at a given index.

        Args:
        - self: The instance of the class.
        - index: The index of the player whose incorporation of points is to be calculated.

        Returns:
        - The incorporation of points for the player at the specified index.

        Explanation:
        - Retrieve the points of the player at the specified index from the player_info attribute.
        - Calculate the total points of all players by summing up the points of each player in player_info.
        - Compute the incorporation of points for the player at the specified index using a formula:
          (L_CONSTANT * (player_points / total_player_points)).
          - L_CONSTANT is a constant factor.
          - player_points is the points of the player at the specified index.
          - total_player_points is the sum of points of all players.
        - Return the incorporation of points for the player at the specified index.
        """
        # Step 1: Get the player inputed points
        player_points = self.player_info[index][3]

        # Step 2: Get the total points of all the players
        total_player_points = sum([player[3] for player in self.player_info])

        # Step 3: Return the quotient multiplied by the L constant
        return (self.L_CONSTANT * (player_points / total_player_points))

    def actual_outcome(self, index):
        return self.player_info[index][2]


    def add_players(self, *args):    
        """
        Method to add players to the game database.

        Args:
            *args: Variable length argument list containing player objects to be added.

        Returns:
            None

        Comments:
            - Loop through each player object provided in the arguments.
            - Insert each player at the beginning of the player data list.
            - Set initial score for each player to 1000.
            - Allow duplicate entries in the player data list.
            - Print the updated player data list.
            - Save the updated player data to a CSV file named "player_data.csv" without indexing.

        """

        # Loop through each player object provided in the arguments.
        for player in args:
            # Insert each player at the beginning of the player data list with an initial score of 1000.
            self.all_player_data.insert(0, player, 1000, allow_duplicates=False)

        # Print the updated player data list.
        print(self.all_player_data)

        # Save the updated player data to a CSV file named "player_data.csv" without indexing.
        self.all_player_data.to_csv("player_data.csv", index=False) 


    def update_csv(self):
        """
        Update the CSV file containing player data based on the current game state.

        Returns:
            None

        Comments:
            - Iterate through each player in the game.
            - Check if the player exists in the player data DataFrame.
            - If the player exists, update their information in the DataFrame.
            - Save the updated player data to a CSV file named "player_data.csv" without indexing.

        """

        # Iterate through each player in the game.
        for player in self.player_info:
            # Check if the player exists in the player data DataFrame.
            if player[0] in self.all_player_data.columns:
                # If the player exists, update their information in the DataFrame.
                self.all_player_data.loc[0, player[0]] = round(player[4], 2)

        # Save the updated player data to a CSV file named "player_data.csv" without indexing.
        self.all_player_data.to_csv("player_data.csv", index=False)

