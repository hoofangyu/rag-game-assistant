class ChatMemory():
    def __init__(self):
        """
        Initializes the ChatMemory instance with an empty dictionary for storing chat histories.
        """
        self.memory = {}

    def check_memory(self, session_id):
        """
        Args:
        - session_id: Unique identifier for a session.

        Returns:
        - True if the session's memory exists, otherwise False.
        """
        return session_id in self.memory
    
    def create_memory(self, session_id):
        """
        Args:
        - session_id: Unique identifier for a session.

        Creates a new empty chat history for the given session ID.
        """
        self.memory[session_id] = []
  
    def get_memory(self, session_id):
        """
        Args:
        - session_id: Unique identifier for a session.

        Returns:
        - A list of chat entries for the session or None if the session has no memory.
        """
        return self.memory.get(session_id)

    def update_memory(self, session_id, query_text, result):
        """
        Args:
        - session_id: Unique identifier for a session.
        - query_text: User's input text.
        - result: Bot's response text.

        Updates the session's chat history with the latest user query and bot response.
        Limits chat history to the 5 most recent entries.
        """
        self.memory[session_id].append({"user": query_text, "bot": result})
        if len(self.memory[session_id]) > 5:
            del self.memory[session_id][0]