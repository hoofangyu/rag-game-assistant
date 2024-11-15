class ChatMemory():
    def __init__(self):
        self.memory = {}

    def check_memory(self, session_id):
        return session_id in self.memory
    
    def create_memory(self, session_id):
        self.memory[session_id] = []
  
    def get_memory(self, session_id):
        return self.memory.get(session_id)

    def update_memory(self, session_id, query_text, result):
        self.memory[session_id].append({"user": query_text, "bot": result})
        print(self.memory)
        if len(self.memory[session_id]) > 5:
            del self.memory[session_id][0]



