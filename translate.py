import re


def extract_number(arg1):
    return re.sub("[^0-9.]", "", "" + arg1 + "")


def mirror(value):
    value = str(value)
    find_y = value.find('y')

    if find_y > -1:
        if value == 'y/2':
            return value
        else:
            find_dash = value.find('/')
            if find_dash > -1:  # for example -> y/2
                return'y-(' + value + ')'
            else:  # for example -> y-37
                return extract_number(value)
    else:  # for example -> 37
        return 'y-' + value

def drawer(depth):  # update for every sliders depth
    safe_space = 10
    if depth > 560+safe_space:  # > 570 -> 560
        length = 560
    elif 560+safe_space > depth > 510+safe_space:  # 570 : 520 -> 510
        length = 510
    elif 510+safe_space > depth > 460+safe_space:  # 520 : 470 -> 460
        length = 460
    elif 460+safe_space > depth > 410+safe_space:  # 470 : 420 -> 410
        length = 410
    elif 410+safe_space > depth > 360+safe_space:  # 420 : 370 -> 360
        length = 360
    elif 360+safe_space > depth > 310+safe_space:  # 370 : 320 -> 310
        length = 310
    else:
        length = 260

    if 285 >= length >= 260:
        raster = [10, 133]  # drill first and last hole in slider
    elif 310 >= length >= 385:
        raster = [10, 165]
    elif 410:
        raster = [10, 229]
    elif 435 >= length >= 485:
        raster = [10, 261]
    elif length == 510 or length == 535:
        raster = [10, 284]
    elif length == 560:
        raster = [10, 325]

    print('adding drawer with length: ' + str(length))
    return length, raster


def material(furniture_thickness, texture):
    furniture_thickness = str(furniture_thickness)
    material = furniture_thickness
    material_laminated = 'MDF18 LAMIN'
    excess_veener = 20
    excess_paint = 10

    if texture == 'oak':
        return 'dąb', material, excess_veener
    elif texture == 'oak-light':
        return 'dąb jasny', material, excess_veener
    elif texture == 'oak-wenge':
        return 'dąb wenge', material, excess_veener
    elif texture == 'oak-white':
        return 'dąb biały', material, excess_veener
    elif texture == 'ash':
        return 'jesion', material, excess_veener
    elif texture == 'walnut':
        return 'orzech', material, excess_veener
    else:
        if furniture_thickness == '18' or furniture_thickness == '19':
            return texture, material_laminated, excess_paint
        else:
            return texture, material, excess_veener
