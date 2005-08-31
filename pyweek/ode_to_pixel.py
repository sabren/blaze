
scale_factor = 64. * 9

def pixel2world(x,y):
    return x / scale_factor,y / scale_factor

def world2pixel(x,y):
    return x * scale_factor ,y * scale_factor


def px2w(x):
    return x / scale_factor

def w2px(x):
    return x * scale_factor


