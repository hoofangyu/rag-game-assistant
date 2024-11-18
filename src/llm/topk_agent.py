from openai import OpenAI
from src.utils import OPENAI_API_KEY

client = OpenAI(api_key = OPENAI_API_KEY)

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

    # Call the OpenAI API to get the response
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts information from user queries."},
            {"role": "user", "content": prompt}
        ]
    )

    output = completion.choices[0].message.content
    print(output)

    try:
        k = int(output.strip()) + 2 # for buffer
    except ValueError:
        k = default_k

    return k