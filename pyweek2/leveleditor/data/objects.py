from object import GameObject

def get_grouped_objects():
    groups = {}
    for object in get_objects():
        groups.setdefault(object.group,[]).append(object)
    return groups

def get_objects():
    objects = []
    
    name = 'Mega Blaster'
    group = 'Weapons'
    sprite = 'blaster.png'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Bastard From HELL'
    group = 'Weapons'
    sprite = 'bastard.png'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Steamer Roaster'
    group = 'Weapons'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Hot Stuff'
    group = 'Weapons'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Burning Hands'
    group = 'Weapons'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Evil Guy'
    group = 'Bosses'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Good guy, but converted to evil'
    group = 'Bosses'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Watery Look'
    group = 'Bosses'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Farter'
    group = 'Bosses'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Blue Tile'
    group = 'Tiles'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite,group))
    
    name = 'Green Tile'
    group = 'Tiles'
    sprite = '/relative/path/to/sprite'
    objects.append(GameObject(name,sprite,group))
    
    return objects
