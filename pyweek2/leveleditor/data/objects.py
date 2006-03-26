from object import GameObject

def get_objects():
    objects = []
    
    name = 'Mega Blaster'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite))
    
    name = 'Bastard From HELL'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite))
    
    
    name = 'Steamer Roaster'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite))
    
    name = 'Hot Stuff'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite))
    return objects
