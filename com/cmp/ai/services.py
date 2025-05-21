from models import tutorial_fields

# 模拟数据库
tutorials = []
id_counter = 0

def create_tutorial(tutorial):
    global id_counter
    id_counter += 1
    tutorial['id'] = id_counter
    tutorials.append(tutorial)
    return tutorial

def get_all_tutorials(title=None):
    if title:
        return [t for t in tutorials if title in t['title']]
    return tutorials

def get_tutorial_by_id(id):
    for tutorial in tutorials:
        if tutorial['id'] == id:
            return tutorial
    return None

def update_tutorial(id, tutorial):
    for idx, t in enumerate(tutorials):
        if t['id'] == id:
            tutorials[idx] = {**t, **tutorial}
            return tutorials[idx]
    return None

def delete_tutorial(id):
    global tutorials
    tutorials = [t for t in tutorials if t['id'] != id]
    return True

def delete_all_tutorials():
    global tutorials
    tutorials = []
    return True

def find_published_tutorials():
    return [t for t in tutorials if t['published']]