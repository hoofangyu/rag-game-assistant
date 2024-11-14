import pandas as pd 

class DescriptionParser:
    def __init__(self, file_path):
        """
        Initializes the DescriptionParser with the file path and column name.
        
        Args:
            file_path (str): The path to the CSV file.
        """
        self.file_path = file_path

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
            f"Link: {row['link']}"
        )
        return parsed_string

    def parse(self):
        """
        Parses the CSV file and returns a list of strings that represents the metadata for each game.
        
        Returns:
            list of str: A list containing formatted strings for each row in the CSV file.
        """
        df = pd.read_csv(self.file_path)
        ls = df.apply(lambda x: self.parse_row(x), axis=1).tolist()
        return ls


    



    