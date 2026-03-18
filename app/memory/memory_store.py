MEMORY = {}

def get_memory(user_id:str):
    return MEMORY.get(user_id,{})

def update_memory(user_id:str , data:dict):
    MEMORY[user_id]=data