from openai import OpenAI
from src.utils import OPENAI_API_KEY

client = OpenAI(api_key = OPENAI_API_KEY)

def prompt_sync(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts information from user queries."},
            {"role": "user", "content": prompt}
        ]
    )

    output = completion.choices[0].message.content
    return output


def get_number_of_results_from_query(query, default_k=5):
    """
    Uses OpenAI's LLM to interpret the user's query and determine the number of results (k).
    
    Args:
        query (str): The user's query.
        default_k (int): The default number of results to return if the user does not specify a number.
    
    Returns:
        int: The number of results to retrieve based on the user's intent.
    """

    prompt = f"""
    You are an intelligent assistant that interprets user queries. Your task is to determine how many results the user is looking for based on their query. 
    If the user specifies a number of results, extract that number as an integer. If the user does not specify a number, return the default number of results: {default_k}.
    
    User Query: "{query}"
    
    How many results is the user looking for? Return only the number of results as an integer and nothing more.
    """

    k = int(prompt_sync(prompt))

    return k

def requires_code_intepretor(query):
    """
    Uses OpenAI's LLM to interpret the user's query and whether a code intepretor is needed.
    
    Args:
        query (str): The user's query.
    
    Returns:
        int: 1 if code intepretor is needed and 0 otherwise
    """

    prompt = f"""
    I have a vector database where each document contains the following information about a game: game title, description, genre, publisher, and system requirements.

    Given a user query about games, determine if the information in the database is sufficient to provide a response or if answering the query requires additional information from an external dataset.

    Considerations:

    Return 0 if the query can be fully answered using the game titles, descriptions, genres, publishers, or system requirements available in the database.
    Return 1 if the query requires information that cannot be directly matched or inferred from the database (e.g., real-world sales data, external reviews, or subjective opinions).
    For recommendations, assume the database can retrieve games matching a genre, title, or related metadata unless explicitly stated otherwise.
    Query: {query}

    Output format:
    <integer>, <reason>
    """

    output = prompt_sync(prompt)
    print(output)
    k = int(output.split(",")[0])

    return k