import pandas as pd 

class DescriptionParser:
    def __init__(self, description_path, ranking_path):
        """
        Initializes the DescriptionParser with the file path and column name.
        
        Args:
            description_path (str): The path to the games description CSV file.
            ranking_path (str): The path to the games ranking CSV file.
        """
        self.description_path = description_path
        self.ranking_path = ranking_path

    def merge_games(self, df1, df2):
        """
        Args:
            df1 (pd.DataFrame): games description df.
            df2 (pd.DataFrame): games ranking df.
        """
        pivoted_df = df2.drop(columns="genre").drop_duplicates(subset = ["game_name", "rank_type"]).pivot(index = "game_name", columns = "rank_type", values = "rank")
        final_df = df1.merge(pivoted_df, how = "left", left_on= "name", right_on = "game_name").rename(columns={'Revenue': 'revenue_rank', 'Review': 'review_rank', 'Sales':'sales_rank'})
        return final_df

    def parse_row(self, row):
        """
        Converts a row from the DataFrame into a formatted string.

        Args:
            row (pd.Series): A row from the DataFrame.
        
        Returns:
            str: A formatted string with metadata information for each game.
        """
        parsed_string = (
            f"Name: {row['name']}\n"
            f"Short Description: {row['short_description']}\n"
            f"Genres: {row['genres']}\n"
            f"Minimum System Requirements: {row['minimum_system_requirement']}\n"
            f"Recommended System Requirements: {row['recommend_system_requirement']}\n"
            f"Release Date: {row['release_date']}\n"
            f"Developer: {row['developer']}\n"
            f"Publisher: {row['publisher']}\n"
            f"Overall Player Rating: {row['overall_player_rating']}\n"
            f"Reviews from Purchased People: {row['number_of_reviews_from_purchased_people']}\n"
            f"English Reviews: {row['number_of_english_reviews']}\n"
            f"Link: {row['link']}\n"
            f"Revenue Ranking: {row['revenue_rank']}\n"
            f"Review Ranking: {row['review_rank']}\n"
            f"Sales Ranking: {row['sales_rank']}\n"
        )
        return parsed_string

    def parse(self):
        """
        Parses the CSV file and returns a list of strings that represents the metadata for each game.
        
        Returns:
            list of str: A list containing formatted strings for each row in the CSV file.
        """
        df1 = pd.read_csv(self.description_path)
        df2 = pd.read_csv(self.ranking_path)
        df = self.merge_games(df1,df2)
        ls = df.apply(lambda x: self.parse_row(x), axis=1).tolist()
        return ls


    



    