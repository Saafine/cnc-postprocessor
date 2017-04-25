#!/usr/bin/env python
# -*- coding: utf-8 -*-
# enable UTF-8 characters in the console

import requests  # used to request webpage source code (you need to download this)
import os  # file creating/renaming
import shutil  # folder deleting
import cnc
import translate
import bom
import acc

from bs4 import BeautifulSoup  # used to analyze webpage source code (you need to download this)


class G:
    unit = 10  # cm to mm
    backwall = 5  # backwall groove
    recess = 5  # frontal recess
    board_support = 55 * unit  # when to use more than 2 connectors (rafixes)
    maximum_tabletop = 260 * unit  # worktop maximum length
    maximum_sockle = 240 * unit  # sockle maximum length
    wide_drawer = 60 * unit  # when drawers needs additional sync to open
    perfect_push = 120 * unit  # desired push to open location
    sockle_raster = 70 * unit  # distance between sockle's keku


class Model:
    url = 'http://meble.design/root/configurations/0202173.txt'
    # used for order folder creation and setting order number
    temp_number = url.rsplit('/', 1)[-1]  # from end to first slash
    web_number = temp_number.rsplit('.', 1)[0]  # from start to full space
    order_folder = r'orders/'+web_number+r'/'
    folders = ['sciana', 'blat', 'dno', 'polka', 'drzwi', 'pionik', 'szuflada']
    order_id = web_number

    source_code = requests.get(url)  # loops, connects to webpage, stores result in variable sourcecode
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    columns = int((soup.find("div", {"id": "load_model_columns"})).string)  # find specific div in the source code, get inside content without html
    height = float((soup.find("div", {"id": "load_model_height"})).string) * G.unit
    width = float((soup.find("div", {"id": "load_model_width"})).string) * G.unit
    depth = float((soup.find("div", {"id": "load_model_depth"})).string) * G.unit
    furniture_thickness = float((soup.find("div", {"id": "load_furniture_thickness"})).string) * G.unit
    sockle_height = float((soup.find("div", {"id": "load_sockle_height"})).string) * G.unit

    active_texture = (soup.find("div", {"id": "load_active_texture"})).string
    active_backwall_texture = (soup.find("div", {"id": "load_active_backwall_texture"})).string
    tabletop_mode = (soup.find("div", {"id": "load_model_tabletop"})).string
    standingByWall = (soup.find("div", {"id": "load_model_standingByWall"})).string

    height_array = (soup.find("div", {"id": "load_model_height_array"})).string
    height_array = height_array.split(";")  # split result into list
    height_array = list(map(float, height_array))  # convert items into float
    height_array = [x * G.unit for x in height_array]  # convert into mm

    width_array = (soup.find("div", {"id": "load_model_width_array"})).string
    width_array = width_array.split(";")
    width_array = list(map(float, width_array))
    width_array = [x * G.unit for x in width_array]  # convert into mm

    depth_array = (soup.find("div", {"id": "load_model_depth_array"})).string
    depth_array = depth_array.split(";")
    depth_array = list(map(float, depth_array))
    depth_array = [x * G.unit for x in depth_array]  # convert into mm

    shelf_array = (soup.find("div", {"id": "load_model_shelf_array"})).string
    shelf_array = shelf_array.split(";")
    shelf_array = list(map(int, shelf_array))

    space_array = []
    for run_col in range(columns):
        space_array.append((soup.find("div", {"id": "load_space_array_" + str(run_col)})).string)
        space_array[run_col] = space_array[run_col].split(";")
        space_array[run_col] = list(map(float, space_array[run_col]))
        space_array[run_col] = [x * G.unit for x in space_array[run_col]]  # convert into mm


class Drawer:  # this is wrong, wrong distance for drillings and bottom fix is wrong also
    thickness = 16  # !update, model.active texture
    slider_fix = 7  # if slider = 450 then drawer's side is 443
    bottom_fix = 15  # distance to sawing plane, !update, only for veenered
    front_lowered = 3  # distance between top of the drawer's front and top of the drawer's side
    width_slider_fix = 41  # fix the drawer's width
    front_z = 'z/2'
    dowel_distance_1 = 32
    back_slider_x = 7
    back_slider_y = 7
    back_slider_diameter = 7
    back_slider_depth = 10

    wall_board_distance = 46  # distance from board's top plane to slider's drilling
    wall_diameter = 4
    wall_depth = 12


class Btm:  # these are board drillings, not walls
    diameter = 18
    depth = 13
    x = 8
    y = 37
    fix_depth = 1
    y_fixed_depth = y + fix_depth


class Mid:  # these are board drillings, not walls
    diameter = 20
    depth = 15
    x = 9.5
    y = 37
    fix_depth = 1
    y_fixed_depth = y + fix_depth


class Top:
    x = 0
    y = 37
    y_dowel = 37+32  # y_cam and pin inherit from Btm


class Sock:
    diameter = 3
    depth = 3
    x = 60  # distance from wall
    y = 65
    raster = 32
    wall_y = x + Model.furniture_thickness/2
    thickness = 18


class Common:
    diameter_pin = 8
    diameter_cam = 15
    diameter_dowel = 8

    depth_pin = 30
    depth_dowel = 25
    depth_cam = 13

    depth_pin_inserted = 12.5
    depth_dowel_inserted = 12.5

    z0 = 9  # Z value for dowel/cam/pin for divider
    z1 = 'z-'+str(z0)  # Z value for dowel/cam/pin
    z1_inserted = Model.furniture_thickness - 9
    x_cam = 34.5


class Wall:
    # Common board variables
    brd_diameter = 5
    brd_depth = 12

    # Bottom boards variables
    btm_fix_x = 8  # distance from bottom's plane to drilling, for Hafele Tab connector
    btm_x = 'x-'+str(Model.sockle_height + btm_fix_x)  # get bottom board position from the ground

    # Middle boards variables
    mid_fix_x = 9.5

    # Hinge variables
    hinge_diameter = 4
    hinge_depth = 13
    hinge_y = 36  # + raster for gtv?

    # Push to Open variables
    push_y_1 = 20
    push_y_2 = 37
    push_diameter = 3
    push_depth = 3

    def get_wall_attributes(self, column, mirror):
        move_start = 0
        if Model.columns > column > 0:
            if mirror:
                if Model.depth_array[column] > Model.depth_array[column-1]:  # if next inside is deeper than previous
                    move_start = Model.depth_array[column] - Model.depth_array[column-1]
            else:
                if Model.depth_array[column] < Model.depth_array[column-1]:
                    move_start = Model.depth_array[column-1] - Model.depth_array[column]

        this_depth = Model.wall[column].depth

        return this_depth, move_start


# varying depths fix
    def drill_btm(self, backwall, mirror, column):
        wall_attr = self.get_wall_attributes(column, mirror)  # returns this wall's depth, move start (difference between neighbouring walls)
        this_depth = wall_attr[0]
        move_start = wall_attr[1]

        if backwall:
            _1 = Btm.y_fixed_depth + move_start
            _2 = (this_depth - G.backwall) / 2 + move_start
            _3 = 'y-'+str(Btm.y+G.backwall)
        else:
            _1 = Btm.y_fixed_depth + move_start
            _2 = this_depth / 2 + move_start
            _3 = 'y-'+str(Btm.y)

        if mirror:
            return translate.mirror(_1), translate.mirror(_2), translate.mirror(_3)
        else:
            return _1, _2, _3

    def drill_top(self, backwall, mirror):
        if backwall:
            _1 = Top.y
            _2 = 'y/2'
            _3 = 'y-'+str(Top.y)
        else:
            _1 = Top.y
            _2 = 'y/2-'+str(G.backwall/2)
            _3 = 'y-'+str(Top.y-G.backwall)

        if mirror:
            return translate.mirror(_1), translate.mirror(_2), translate.mirror(_3)
        else:
            return _1, _2, _3

    def drill_dowel(self, backwall, mirror):  # drill_top also
        if backwall:
            _1 = Top.y_dowel
            _2 = 'y-'+str(Top.y_dowel)
        else:
            _1 = Top.y_dowel
            _2 = 'y-'+str(Top.y_dowel-G.backwall)

        if mirror:
            return translate.mirror(_1), translate.mirror(_2)
        else:
            return _1, _2

    def drill_mid(self, backwall, mirror, recess, column):
        wall_attr = self.get_wall_attributes(column, mirror)  # returns this wall's depth, move start (difference between neighbouring walls)
        this_depth = wall_attr[0]
        move_start = wall_attr[1]

        # drilling in the middle of a shelf -> on wall, half the width, add half recess and minus backwall if necessary
        if backwall:
            if recess:  # 3
                _1 = move_start + Mid.y + G.recess
                _2 = (this_depth-G.recess-G.backwall)/2 + move_start + G.recess
                _3 = 'y-'+str(Mid.y + G.backwall)
            else:  # 4
                _1 = move_start + Mid.y_fixed_depth
                _2 = (this_depth - G.backwall) / 2 + move_start
                _3 = 'y-'+str(Mid.y+G.backwall)
        else:
            if recess:  # 1
                _1 = move_start + Mid.y + G.recess
                _2 = (this_depth - G.recess) / 2 + move_start + G.recess
                _3 = 'y-' + str(Mid.y)
            else:  # 2
                _1 = move_start + Mid.y_fixed_depth
                _2 = this_depth / 2 + move_start
                _3 = 'y-'+str(Mid.y)

        if mirror:
            return translate.mirror(_1), translate.mirror(_2), translate.mirror(_3)
        else:
            return _1, _2, _3

    def drill_drawer(self, mirror, column, raster):
        wall_attr = self.get_wall_attributes(column, mirror)
        move_start = wall_attr[1]

        _1 = raster[0] + move_start
        _2 = raster[1] + move_start

        if mirror:
            return translate.mirror(_1), translate.mirror(_2)
        else:
            return _1, _2


class Door:
    thickness = 18
    free_space = 4   # desired space between two neighbouring doors
    cover = (Model.furniture_thickness - free_space) / 2
    hinge_raster_screw_wall = 32
    hinge_diameter_cup = 35
    hinge_depth_cup = 13
    hinge_y_cup = 22.5
    hinge_y_screw = 28.5
    hinge_diameter_screw = 3
    hinge_depth_screw = 3
    hinge_raster_screw_door = 48

    distance1 = 70  # distance from boards plane to center of first drilling in wall
    distance_push = 55  # distance from boards plane to center of push to open drilling in wall
    minimum_hinge_space = distance1 + hinge_raster_screw_wall / 2 + Model.furniture_thickness / 2  # minimum distance from middle of a board to center of a hinge
    minimum_push_space = distance_push + Model.furniture_thickness / 2

    # push_diameter = 3
    # push_depth = 3
    # push_y = 10

    flap_hinge_door_y = 25
    flap_hinge_board_y = 7.5

    flap_hinge_wall_x = 45  # middle of the hinge, distance from the wall's plane
    flap_hinge_diameter = 35
    flap_hinge_depth = 11.5

    def required_hinges(self, height):
        if height > 2400:
            hinges = 5
        elif 2400 > height > 2000:
            hinges = 4
        elif 2000 > height > 1600:
            hinges = 3
        else:
            hinges = 2
        return hinges


class Divider:
    y_cam = 37
    y_dowel = y_cam + 32
    recess = 5  # from bottom board if already recessed
    recess_extended = 10  # from bottom board if not recessed


class DoorObject:
    def __init__(self, column, start, end, doortype, texture, column_end, open):  # run every time when creating object
        self.column = int(column)
        self.start = int(start)
        self.end = int(end)
        self.doortype = doortype
        self.texture = texture
        self.column_end = int(column_end)
        self.open = str(open)
        self.topboard = Model.board[self.column-1][self.end-1].y - Model.furniture_thickness/2
        self.botboard = Model.board[self.column-1][self.start-1].y + Model.furniture_thickness/2
        self.thickness = Door.thickness
        if self.doortype == 'door' or self.doortype == 'drawer' or self.doortype == 'flap':
            self.height = self.topboard - self.botboard + 2 * Door.cover
            self.width = Model.width_array[self.column-1] + 2 * Door.cover
        elif self.doortype == 'doubleLEFT' or self.doortype == 'doubleRIGHT':
            self.height = self.topboard - self.botboard + 2 * Door.cover
            self.width = (Model.width_array[self.column-1] + 2 * Door.cover)/2 - Door.free_space/2

        self.startY = round(Model.board[self.column - 1][self.start - 1].y, 1)
        self.endY = round(Model.board[self.column - 1][self.end - 1].y, 1)
        self.hinges = []
        self.hinges_wall = []
        # self.pushToOpen = False
        self.pushToOpen_wall = False

        if Model.board[self.column-1][self.start-1].recess == True:  # update board's depth below doors
            Model.board[self.column-1][self.start-1].recess = False
            Model.board[self.column-1][self.start-1].depth += G.backwall

        if Model.board[self.column-1][self.end-1].recess == True:  # update board's depth above doors
            Model.board[self.column-1][self.end-1].recess = False
            Model.board[self.column-1][self.end-1].depth += G.backwall

        if self.doortype == 'door':
            # CALCULATE PUSH TO OPEN
            if self.topboard > G.perfect_push > self.botboard:
                temp_push = G.perfect_push
                for shelf in range(self.start - 1, self.end):  # check every board that is being covered by doors
                    board_position = Model.board[self.column - 1][shelf].y
                    if board_position + Door.minimum_push_space > temp_push > board_position - Door.minimum_push_space:  # check upper and lower space for conflict
                        if board_position + Door.minimum_push_space > temp_push:  # check if board is above conflict
                            temp_push = board_position - Door.minimum_push_space  # update push position to avoid conflict
                        else:  # check if board is below conflict
                            temp_push = board_position + Door.minimum_push_space
                        break
            elif G.perfect_push > self.topboard:
                temp_push = self.topboard - Door.minimum_push_space
            elif G.perfect_push < self.botboard:
                temp_push = self.botboard + Door.minimum_push_space
            self.pushToOpen_wall = temp_push  # set position of Push-To-Open on wall
            # self.pushToOpen = temp_push - self.botboard + Door.cover

            # CALCULATE REQUIRED HINGES
            requested_hinge_position = []
            get_required_hinges = Door().required_hinges(self.height)
            if get_required_hinges == 3:
                requested_hinge_position.append(self.botboard+(self.topboard - self.botboard)/2)  # hinge between in the middle of two planes
            elif get_required_hinges == 4:
                requested_hinge_position.append(self.botboard+(self.topboard - self.botboard)*1/3)
                requested_hinge_position.append(self.botboard + (self.topboard - self.botboard) * 2 / 3)
            elif get_required_hinges == 5:
                requested_hinge_position.append(self.botboard + (self.topboard - self.botboard) * 1 / 4)
                requested_hinge_position.append(self.botboard + (self.topboard - self.botboard) * 2 / 4)
                requested_hinge_position.append(self.botboard + (self.topboard - self.botboard) * 3 / 4)

            # calculate hinge position on wall
            for check_hinge in range(len(requested_hinge_position)):  # check every hinge
                for shelf in range(self.start-1, self.end):  # check every board that is being covered by doors
                    board_position = Model.board[self.column-1][shelf].y
                    check_conflict = requested_hinge_position[check_hinge]
                    if board_position + Door.minimum_hinge_space > check_conflict > board_position - Door.minimum_hinge_space:  # check upper and lower space for conflict
                        if board_position + Door.minimum_hinge_space > check_conflict:  # check if board is above conflict
                            requested_hinge_position[check_hinge] = board_position + Door.minimum_hinge_space  # update hinges position to avoid conflict
                        else:
                            requested_hinge_position[check_hinge] = board_position - Door.minimum_hinge_space
                        break

            # add standard hinges on top and bottom
            requested_hinge_position.append(self.startY + Door.minimum_hinge_space)  # append standard hinge on top, adjust for space
            requested_hinge_position.append(self.endY - Door.minimum_hinge_space)  # append standard hinge on bottom, adjust for space
            self.hinges_wall.extend(requested_hinge_position)

            # calculate hinge position on door
            for hinge_position in requested_hinge_position:
                hinge_cup = hinge_position - self.botboard + Door.cover  # hinge position on door - (get top plane of bottom board - adjust for door cover)
                self.hinges.append(hinge_cup)

            if self.open == 'right':  # DOOR OPENING RIGHT
                Model.wall[self.column].hasDoorRight.append(len(Model.door))
                Model.wall[self.column-1].hasPushRight.append(len(Model.door))
            elif self.open == 'left':  # DOOR OPENING LEFT
                Model.wall[self.column-1].hasDoorLeft.append(len(Model.door))
                Model.wall[self.column].hasPushLeft.append(len(Model.door))

        if self.doortype == 'drawer':
            slider_info = translate.drawer(Model.depth_array[self.column-1] - G.backwall)
            self.slider = slider_info[0]
            self.raster = slider_info[1]
            self.drawer_side_height = round(0.7 * Model.space_array[self.column-1][self.start-1])
            self.drawer_front_height = self.drawer_side_height - Drawer.bottom_fix - Drawer.front_lowered
            self.drawer_side_depth = self.slider - Drawer.slider_fix
            self.drawer_front_width = round(Model.width_array[self.column-1], 1) - Drawer.width_slider_fix

            Model.wall[self.column - 1].hasDrawerStart.append(len(Model.door))
            Model.wall[self.column_end].hasDrawerEnd.append(len(Model.door))

        if self.doortype == 'flap':
            for run_col in range(self.column, self.column_end):  # check remaining columns
                for run_shelf in range(1, Model.shelf_array[run_col]+1):
                    if (Model.board[run_col][run_shelf].y == self.startY or Model.board[run_col][run_shelf].y == self.endY) and Model.board[run_col][run_shelf].recess == True:
                        Model.board[run_col][run_shelf].recess = False
                        Model.board[run_col][run_shelf].depth += G.backwall
            if self.open == 'bot':
                Model.board[self.column - 1][self.start-1].hasFlapOnTop = True
            elif self.open == 'top':
                Model.board[self.column - 1][self.end-1].hasFlapOnBottom = True
            self.hinges.append(Door.flap_hinge_wall_x + Door.cover)


class HangerObject:
    def __init__(self, column, start, type):
        self.column = int(column)
        self.start = int(start)
        self.type = str(type)


class DividerObject:
    def __init__(self, column, start, position):
        self.column = int(column)
        self.start = int(start)
        self.thickness = Model.furniture_thickness
        self.height = Model.space_array[self.column-1][self.start-1]
        self.depth = Model.depth_array[self.column-1] - G.backwall - G.recess - Divider.recess
        self.position = str(position)

        # used for board drillings
        Model.board[self.column - 1][self.start - 1].hasDividerOnTop.append(len(Model.divider))  # update board below divider
        Model.board[self.column - 1][self.start].hasDividerOnBottom.append(len(Model.divider))  # update board above divider
        self.get_recess_bot = Divider.recess if Model.board[self.column-1][self.start-1].recess else Divider.recess_extended  # checks if board below recessed
        self.get_recess_top = Divider.recess if Model.board[self.column-1][self.start].recess else Divider.recess_extended  # checks if board above recessed

        if self.start == Model.shelf_array[self.column-1]+1:  # check if divider belongs to worktop
            for run_worktop in range(len(Model.tabletop)):
                if Model.tabletop[run_worktop].start < self.column <= Model.tabletop[run_worktop].end:  # check to which worktop divider belongs
                    half_space = Model.width_array[self.column-1]/2

                    if Model.tabletop[run_worktop].cover == 'LEFT' or Model.tabletop[run_worktop].cover == 'BOTH':  # check where tabletop begins, adjust for type
                        top_start_wall = Model.wall[Model.tabletop[run_worktop].start].x - Model.furniture_thickness/2
                    else:
                        top_start_wall = Model.wall[Model.tabletop[run_worktop].start].x + Model.furniture_thickness/2

                    top_end_wall = Model.wall[self.column-1].x + Model.furniture_thickness/2  # check where divider's space begins, get right wall's plane
                    move_start = top_end_wall - top_start_wall  # calculate movement on tabletop
                    divider_middle_position = move_start + half_space  # get final divider middle position
                    Model.tabletop[run_worktop].hasDivider.extend([len(Model.divider), divider_middle_position])


class BoardObject:
    def __init__(self, column, positionY):
        self.column = int(column)
        self.width = Model.width_array[self.column-1]
        self.y = float(positionY)
        self.thickness = Model.furniture_thickness
        self.hasFlapOnTop = False
        self.hasFlapOnBottom = False
        self.hasDividerOnTop = []
        self.hasDividerOnBottom = []
        self.hasSockle = []

        if len(Model.board[column-1]) == 0:  # check for bottom board
            self.depth = Model.depth_array[self.column - 1] - G.backwall
            self.recess = False
        elif len(Model.board[column-1]) == Model.shelf_array[column-1]+1:  # check for top board
            self.depth = Model.depth_array[self.column - 1] - G.backwall
            self.recess = False
        else:  # check for middle board
            self.depth = (Model.depth_array[self.column-1]) - 2 * G.backwall
            self.recess = True


class WallObject:
    def __init__(self, column, height, depth):  # run every time when creating object
        self.column = int(column)
        self.hasDoorRight = []  # check if has door on the right side of wall
        self.hasDoorLeft = []
        self.hasDrawerStart = []
        self.hasDrawerEnd = []
        self.hasPushLeft = []
        self.hasPushRight = []
        self.hasSockle = False

        if Model.tabletop_mode == 'between':
            self.height = float(height)
            self.reduced = False
        else:
            # MODE 1 - tabletop covering wall
            self.height = float(height)-Model.furniture_thickness
            self.reduced = True
            if 0 < self.column < Model.columns:

                if self.column/2 % 1 != 0:
                    if Model.height_array[self.column] > Model.height_array[self.column-1]:
                        if Model.depth_array[self.column] < Model.depth_array[self.column-1]:
                            self.height = float(height)
                            self.reduced = False
                    if Model.height_array[self.column] < Model.height_array[self.column-1]:
                        if Model.depth_array[self.column] > Model.depth_array[self.column-1]:
                            self.height = float(height)
                            self.reduced = False
                    if Model.height_array[self.column] == Model.height_array[self.column-1]:
                        if Model.depth_array[self.column] != Model.depth_array[column-1]:
                            self.height = float(height)
                            self.reduced = False

                if self.column/2 % 1 == 0:
                    if Model.height_array[self.column] < Model.height_array[self.column-1]:
                        if Model.depth_array[self.column] > Model.depth_array[self.column-1]:
                            self.height = float(height)
                            self.reduced = False
                    if Model.height_array[self.column] > Model.height_array[self.column-1]:
                        if Model.depth_array[self.column] < Model.depth_array[self.column-1]:
                            self.height = height
                            self.reduced = False
                    if Model.height_array[self.column] == Model.height_array[self.column-1]:
                        if Model.depth_array[self.column] != Model.depth_array[self.column-1]:
                            self.height = float(height)
                            self.reduced = False

        if self.column == 0 or self.column == Model.columns:
            self.depth = float(depth)
            self.backwall = True
        else:
            if Model.height_array[self.column-1] == Model.height_array[self.column]:
                self.depth = float(depth) - G.backwall
                self.backwall = False
            else:
                self.depth = float(depth)
                self.backwall = True

        if self.column == 0:
            self.x = 0
        else:
            self.x = Model.wall[len(Model.wall) - 1].x + Model.width_array[len(Model.wall) - 1] + Model.furniture_thickness


class TableTopObject:
    def __init__(self, start, end, cover):  # run every time when creating object
        self.start = start
        self.end = end
        self.thickness = Model.furniture_thickness
        self.depth = Model.depth_array[start]
        self.hasDivider = []
        self.cover = cover

        a = Model.wall[end].x - Model.wall[start].x + Model.furniture_thickness
        b = Model.wall[end].x - Model.wall[start].x
        c = b - Model.furniture_thickness

        if cover == 'BOTH':
            self.width = a
        elif cover == 'NONE':
            self.width = c
            self.depth -= G.backwall
        elif cover == 'LEFT' or cover == 'RIGHT':
            self.width = b


class SockleObject:
    def __init__(self, start, end):
        self.height = Model.sockle_height
        self.width = Model.wall[end].x - Model.wall[start].x - Model.furniture_thickness
        self.thickness = Sock.thickness


def sockle_builder():
    Model.sockletype = 'joint'
    if Model.sockletype == 'joint':
        temp_sockles = [0, 1]
        for counter in range(Model.columns-1):
            get_start = temp_sockles[len(temp_sockles) - 2]  # get wall start position
            get_end = temp_sockles[len(temp_sockles)-1]+1  # get wall end position
            sockle_width = Model.wall[get_end].x - Model.wall[get_start].x - Model.furniture_thickness

            if sockle_width <= G.maximum_sockle and Model.depth_array[counter] == Model.depth_array[counter+1]:
                temp_sockles[len(temp_sockles)-1] += 1  # widen sockle
            else:
                temp_sockles += [get_end-1, get_end]  # create sockle

        for run_sockle in range(0, len(temp_sockles), 2):  # run for every sockle (starting wall, ending wall)
            final_start = temp_sockles[run_sockle]
            final_end = temp_sockles[run_sockle+1]
            Model.sockle.append(SockleObject(final_start, final_end))
            for update_wall in range(temp_sockles[run_sockle]+1, temp_sockles[run_sockle+1]):  # get walls that being covered by sockle, for example: sockle = [0,3] -> then walls [1,2]
                Model.wall[update_wall].hasSockle = True

        # Calculate number of sockle supporters
        requested_sockle = []
        for run_sockle in range(0, len(temp_sockles), 2):
            sockle_width = Model.wall[temp_sockles[run_sockle+1]].x - Model.wall[temp_sockles[run_sockle]].x - Model.furniture_thickness
            get_support_distance = (sockle_width - 2 * Sock.x)  # distance between 2 standard sockle supporters
            count_support = int(get_support_distance / G.sockle_raster)  # round down to nearest integer
            additional_support_raster = get_support_distance / count_support if count_support > 0 else 0  # avoid division by 0

            temp_sockle_drilling = Sock.x
            for x in range(count_support):
                temp_sockle_drilling += additional_support_raster
                temp_wall_conflict = Model.wall[temp_sockles[run_sockle]].x + temp_sockle_drilling + Model.furniture_thickness/2
                requested_sockle += [temp_wall_conflict]  # sockle position from starting wall

            for check_wall in range(temp_sockles[run_sockle] + 1, temp_sockles[run_sockle + 1]):  # check every wall between sockle
                for check_conflict in range(len(requested_sockle)):
                    if Model.wall[check_wall].x + 2*Sock.wall_y < requested_sockle[check_conflict]:
                        break   # no need to check further walls

                    if Model.wall[check_wall].x + Sock.wall_y > requested_sockle[check_conflict] > Model.wall[check_wall].x - Sock.wall_y:  # if conflict with wall found
                        if Model.wall[check_wall].x + Sock.wall_y > requested_sockle[check_conflict]:
                            move_sockle = Model.wall[check_wall].x + Sock.wall_y - requested_sockle[check_conflict]
                            requested_sockle[check_conflict] += move_sockle
                            requested_sockle[check_conflict-1] += move_sockle
                        else:
                            move_sockle = Model.wall[check_wall].x - Sock.wall_y - requested_sockle[check_conflict]
                            requested_sockle[check_conflict] -= move_sockle
                            requested_sockle[check_conflict-1] -= move_sockle

        # Assign sockle supporters to their btm boards
        for run_sockle in range(0, len(temp_sockles), 2):  # run for every sockle (starting wall, ending wall)
            for update_btm in range(temp_sockles[run_sockle], temp_sockles[run_sockle + 1]):  # get walls that being covered by sockle, for example: sockle = [0,3] -> then walls [1,2]
                get_btm_start = Model.wall[update_btm].x
                get_btm_end = Model.wall[update_btm+1].x

                for assign_drilling in range(len(requested_sockle)):
                    wall_drilling = requested_sockle[assign_drilling]
                    if get_btm_end < wall_drilling:  # if drilling doesnt belong here
                        break
                    if get_btm_start < wall_drilling < get_btm_end:  # check if support belongs to btm board
                        btm_drilling = wall_drilling - get_btm_start - Model.furniture_thickness/2
                        Model.board[update_btm][0].hasSockle.append(btm_drilling)

                btm_start_sockle = temp_sockles[run_sockle]  # btm board where sockle starts
                btm_end_sockle = temp_sockles[run_sockle + 1] - 1  # btm board where sockle ends
                btm_all = Model.board[update_btm][0].hasSockle
                if update_btm == btm_start_sockle:
                    btm_all.insert(0, Sock.x)  # insert standard support at the beginning
                if update_btm == btm_end_sockle:  # append standard support or update if already exists
                    btm_width = Model.board[btm_end_sockle][0].width
                    if btm_all[len(btm_all)-1] + 1.5 * Sock.x > btm_width:
                        btm_all[len(btm_all) - 1] = btm_width - Sock.x
                    else:
                        btm_all.append(btm_width - Sock.x)


def worktop_builder():
    if Model.tabletop_mode == 'over':
        temp_tabletops = [0, 1]
        for x in range(1, Model.columns):
            get_start = temp_tabletops[len(temp_tabletops)-2]
            get_end = temp_tabletops[len(temp_tabletops) - 1]
            tabletop_width = Model.wall[get_end + 1].x - Model.wall[get_start].x
            if tabletop_width <= G.maximum_tabletop and Model.depth_array[x-1] == Model.depth_array[x] and Model.height_array[x-1] == Model.height_array[x]:
                temp_tabletops[len(temp_tabletops) - 1] += 1
            else:
                temp_tabletops += [get_end, get_end + 1]

        tabletops_number = len(temp_tabletops)
        for run_tabletops in range(0, tabletops_number, 2):
            start = temp_tabletops[run_tabletops]
            end = temp_tabletops[run_tabletops+1]
            start_reduced = Model.wall[start].reduced
            this_height = Model.height_array[start]
            prev_height = Model.height_array[start-1] if start != 0 else False
            next_height = Model.height_array[end] if end != Model.columns else False

            if start == 0:
                cover_left = True
            else:
                if start_reduced and Model.tabletop[len(Model.tabletop)-1].cover != 'RIGHT' and Model.tabletop[len(Model.tabletop)-1].cover != 'BOTH':
                    cover_left = True
                elif this_height > prev_height:  # fix for wall-e
                    cover_left = True
                else:
                    cover_left = False

            if end == Model.columns:
                cover_right = True
            else:
                cover_right = True if this_height > next_height else False

            if cover_left == True and cover_right == True:
                cover = 'BOTH'
            elif cover_left == False and cover_right == False:
                cover = 'NONE'
            elif cover_left == True and cover_right == False:
                cover = 'LEFT'
            elif cover_left == False and cover_right == True:
                cover = 'RIGHT'

            Model.tabletop.append(TableTopObject(start, end, cover))
    else:
        for run_tabletops in range(Model.columns):
            Model.tabletop.append(TableTopObject(run_tabletops, run_tabletops+1, 'NONE'))


def load_objects():
    Model.wall = []
    for run_col in range(Model.columns+1):
        if run_col == 0:  # print('building first wall')
            Model.wall.append(WallObject(run_col, Model.height_array[run_col], Model.depth_array[run_col]))
            # print('this is first wall ' + str(run_col), str(Model.height_array[run_col]), str(Model.depth_array[run_col]))
            # print('backwall missing')

        if 0 < run_col < Model.columns:  #print('building inner wall')
           if Model.height_array[run_col] <= Model.height_array[run_col-1]: #if this height is <= previous height
               if Model.depth_array[run_col-1] >= Model.depth_array[run_col]: #if this depth <= previous depth
                   Model.wall.append(WallObject(run_col, Model.height_array[run_col-1], Model.depth_array[run_col-1]))
               else:
                    difference_in_height = Model.height_array[run_col-1] - Model.height_array[run_col]
                    depth = Model.depth_array[run_col-1]
                    Model.wall.append(WallObject(run_col, Model.height_array[run_col], Model.depth_array[run_col]))
                    if Model.height_array[run_col] < Model.height_array[run_col-1]: # skip making wall-e if this column height equals previous one.
                        print('walle missing')
           else:  # if this height is > previous height
                if Model.depth_array[run_col-1] > Model.depth_array[run_col]:
                   difference_in_height = Model.height_array[run_col] - Model.height_array[run_col-1]
                   depth = Model.depth_array[run_col]
                   Model.wall.append(WallObject(run_col, Model.height_array[run_col-1], Model.depth_array[run_col-1]))
                   print('walle missing')
                else:
                   Model.wall.append(WallObject(run_col, Model.height_array[run_col], Model.depth_array[run_col]))
        if run_col == Model.columns: #print('building last wall')
            Model.wall.append(WallObject(run_col, Model.height_array[run_col-1], Model.depth_array[run_col-1]))
            if (run_col == 5):
                print('this is sixth wall ' + str(run_col), str(Model.height_array[run_col-1]), str(Model.depth_array[run_col-1]))

    Model.board = []
    for run_col in range(Model.columns):
        Model.board.append([])
        positionY = Model.sockle_height + Model.furniture_thickness / 2  # build bottom board
        Model.board[run_col].append(BoardObject((run_col + 1), positionY))  # build bottom board
        for run_shelf in range(Model.shelf_array[run_col]+1):
            positionY = Model.furniture_thickness + Model.board[run_col][run_shelf].y + Model.space_array[run_col][run_shelf]  # positionY parses middle axis position of the object
            Model.board[run_col].append(BoardObject((run_col + 1), positionY))  # build middle board
        Model.board[run_col].append(BoardObject((run_col + 1), Model.height_array[run_col] - Model.furniture_thickness / 2))  # build top board

    Model.tabletop = []
    worktop_builder()

    counter = 0
    Model.door = []
    while Model.soup.find("div", {"id": "load_door_object_" + str(counter)}):
        temp_door = (Model.soup.find("div", {"id": "load_door_object_" + str(counter)})).string
        temp_door = temp_door.split(",")
        Model.door.append(DoorObject(temp_door[0], temp_door[1], temp_door[2], temp_door[3], temp_door[4], temp_door[5], temp_door[6]))  # column,start,end,type,texture,column_end,open
        counter += 1

    counter = 0
    Model.hanger = []
    while Model.soup.find("div", {"id": "load_hanger_object_" + str(counter)}):
        temp_hanger = (Model.soup.find("div", {"id": "load_hanger_object_" + str(counter)})).string
        temp_hanger = temp_hanger.split(",")
        Model.hanger.append(HangerObject(temp_hanger[0], temp_hanger[1], temp_hanger[2]))  # column,start,type
        counter += 1

    counter = 0
    Model.divider = []
    while Model.soup.find("div", {"id": "load_divider_object_" + str(counter)}):
        temp_divider = (Model.soup.find("div", {"id": "load_divider_object_" + str(counter)})).string
        temp_divider = temp_divider.split(",")
        Model.divider.append(DividerObject(temp_divider[0], temp_divider[1], temp_divider[2]))  # column,start,position
        counter += 1

    Model.sockle = []
    sockle_builder()


def drilling_wall_btm(file, column, backwall, mirror):  # column -> for mirror walls consider previous column
    btm_y = Wall().drill_btm(backwall, mirror, column)  # get y possition, send backwall/mirror info
    temp_column = column - 1 if mirror else column

    file.write(cnc.Woodwop().ww_drilling(Wall.btm_x, btm_y[0], Wall.brd_diameter, Wall.brd_depth))
    if Model.depth_array[temp_column] > G.board_support:  # check if additional drilling needed
        file.write(cnc.Woodwop().ww_drilling(Wall.btm_x, btm_y[1], Wall.brd_diameter, Wall.brd_depth))
    file.write(cnc.Woodwop().ww_drilling(Wall.btm_x, btm_y[2], Wall.brd_diameter, Wall.brd_depth))


def drilling_wall_mid(file, column, shelf, backwall, mirror):
    temp_column = column - 1 if mirror else column
    mid_x = 'x-' + str(Model.board[temp_column][shelf].y - Model.furniture_thickness / 2 + Wall.mid_fix_x)  # get x position
    mid_y = Wall().drill_mid(backwall, mirror, Model.board[temp_column][shelf].recess, column)  # get y position, send ifMirror, ifBackwall, ifRecessed, send column for depth check

    file.write(cnc.Woodwop().ww_drilling(mid_x, mid_y[0], Wall.brd_diameter, Wall.brd_depth))
    if Model.depth_array[temp_column] > G.board_support:  # check if additional drilling needed
        file.write(cnc.Woodwop().ww_drilling(mid_x, mid_y[1], Wall.brd_diameter, Wall.brd_depth))
    file.write(cnc.Woodwop().ww_drilling(mid_x, mid_y[2], Wall.brd_diameter, Wall.brd_depth))


def drilling_wall_top(file, column, backwall, mirror):
    if mirror:
        for x in range(len(Model.tabletop)):
            if column == Model.tabletop[x].end:
                if Model.tabletop[x].cover == 'RIGHT' or Model.tabletop[x].cover == 'BOTH':
                    drill_mode = 'A'
                else:
                    drill_mode = 'B'
                break
            else:
                drill_mode = 'C'
    else:
        for x in range(len(Model.tabletop)):
            if Model.tabletop[x].start <= column < Model.tabletop[x].end:
                if Model.tabletop[x].start == column:
                    if Model.tabletop[x].cover == 'LEFT' or Model.tabletop[x].cover == 'BOTH':
                        drill_mode = 'A'
                    else:
                        drill_mode = 'B'
                    break
                else:
                    drill_mode = 'A'

    temp_column = column - 1 if mirror else column
    if drill_mode == 'A':
        top_y = Wall().drill_top(backwall, mirror)  # btm board and top board have the same distances on y
        top_y_dowel = Wall().drill_dowel(backwall, mirror)

        file.write(cnc.Woodwop().ww_horizontal_drilling(Top.x, top_y[0], Common.z1, Common.diameter_pin, Common.depth_pin))  # horizontal drilling for pin
        file.write(cnc.Woodwop().ww_drilling(Common.x_cam, top_y[0], Common.diameter_cam, Common.depth_cam))  # vertical drilling for cam
        file.write(cnc.Woodwop().ww_horizontal_drilling(Top.x, top_y_dowel[0], Common.z1, Common.diameter_dowel, Common.depth_dowel))  # horizontal drilling for dowel
        if Model.depth_array[temp_column] > G.board_support:  # check if additional drilling needed
            file.write(cnc.Woodwop().ww_horizontal_drilling(Top.x, top_y[1], Common.z1, Common.diameter_pin, Common.depth_pin))
            file.write(cnc.Woodwop().ww_drilling(Common.x_cam, top_y[1], Common.diameter_cam, Common.depth_cam))  # vertical drilling for cam
        file.write(cnc.Woodwop().ww_horizontal_drilling(Top.x, top_y_dowel[1], Common.z1, Common.diameter_dowel, Common.depth_dowel))
        file.write(cnc.Woodwop().ww_horizontal_drilling(Top.x, top_y[2], Common.z1, Common.diameter_pin, Common.depth_pin))
        file.write(cnc.Woodwop().ww_drilling(Common.x_cam, top_y[2], Common.diameter_cam, Common.depth_cam))  # vertical drilling for cam
    if drill_mode == 'B':
        mid_y = Wall().drill_mid(backwall, mirror, False, column)
        mid_x = 'x-' + str(Model.board[temp_column][Model.shelf_array[temp_column]+1].y - Model.furniture_thickness / 2 + Wall.mid_fix_x)  # get x position for mid board type drilling
        file.write(cnc.Woodwop().ww_drilling(mid_x, mid_y[0], Wall.brd_diameter, Wall.brd_depth))
        if Model.depth_array[temp_column] > G.board_support:
            file.write(cnc.Woodwop().ww_drilling(mid_x, mid_y[1], Wall.brd_diameter, Wall.brd_depth))
        file.write(cnc.Woodwop().ww_drilling(mid_x, mid_y[2], Wall.brd_diameter, Wall.brd_depth))


def drilling_wall_door(file, column, side):
    if side == 'LEFT':
        for door_index in Model.wall[column].hasDoorRight:
            for hinge_position in Model.door[door_index].hinges_wall:
                file.write(cnc.Woodwop().ww_drilling('x-' + str(hinge_position-Door.hinge_raster_screw_wall/2), 'y-' + str(Wall.hinge_y), Wall.hinge_diameter, Wall.hinge_depth))  # drill in wall
                file.write(cnc.Woodwop().ww_drilling('x-' + str(hinge_position+Door.hinge_raster_screw_wall/2), 'y-' + str(Wall.hinge_y), Wall.hinge_diameter, Wall.hinge_depth))

    if side == 'RIGHT':
        for door_index in Model.wall[column].hasDoorLeft:
            for hinge_position in Model.door[door_index].hinges_wall:
                file.write(cnc.Woodwop().ww_drilling('x-' + str(hinge_position-Door.hinge_raster_screw_wall/2), Wall.hinge_y, Wall.hinge_diameter, Wall.hinge_depth))  # drill in wall
                file.write(cnc.Woodwop().ww_drilling('x-' + str(hinge_position+Door.hinge_raster_screw_wall/2), Wall.hinge_y, Wall.hinge_diameter, Wall.hinge_depth))


def drilling_wall_push_to_open(file, column, side):
    if side == 'LEFT':
        for door_index in Model.wall[column].hasPushLeft:
            push_position = Model.door[door_index].pushToOpen_wall
            file.write(cnc.Woodwop().ww_drilling('x-' + str(push_position), 'y-'+str(Wall.push_y_1), Wall.push_diameter, Wall.push_depth))
            file.write(cnc.Woodwop().ww_drilling('x-' + str(push_position), 'y-'+str(Wall.push_y_2), Wall.push_diameter, Wall.push_depth))
    if side == 'RIGHT':
        for door_index in Model.wall[column].hasPushRight:
            push_position = Model.door[door_index].pushToOpen_wall
            file.write(cnc.Woodwop().ww_drilling('x-' + str(push_position), Wall.push_y_1, Wall.push_diameter, Wall.push_depth))
            file.write(cnc.Woodwop().ww_drilling('x-' + str(push_position), Wall.push_y_2, Wall.push_diameter, Wall.push_depth))


def drilling_wall_drawer(file, column, mirror):
    if mirror:
        for door_index in Model.wall[column].hasDrawerEnd:
            set_position = Model.door[door_index].botboard + Drawer.wall_board_distance
            raster = Model.door[door_index].raster
            position_y = Wall().drill_drawer(mirror, column, raster)
            file.write(cnc.Woodwop().ww_drilling('x-'+str(set_position), position_y[0], Drawer.wall_diameter, Drawer.wall_depth))
            file.write(cnc.Woodwop().ww_drilling('x-'+str(set_position), position_y[1], Drawer.wall_diameter, Drawer.wall_depth))
    else:
        for door_index in Model.wall[column].hasDrawerStart:
            set_position = Model.door[door_index].botboard + Drawer.wall_board_distance
            raster = Model.door[door_index].raster
            position_y = Wall().drill_drawer(mirror, column, raster)
            file.write(cnc.Woodwop().ww_drilling('x-'+str(set_position), position_y[0], Drawer.wall_diameter, Drawer.wall_depth))
            file.write(cnc.Woodwop().ww_drilling('x-'+str(set_position), position_y[1], Drawer.wall_diameter, Drawer.wall_depth))


def generate_walls():
    for run_col in range(Model.columns + 1):
        wall_type1 = 'Niska' if Model.wall[run_col].reduced else 'Wysoka'
        wall_type2 = 'Gleboka' if Model.wall[run_col].backwall else 'Plytka'

        f = open(Model.order_folder+'sciana/sciana_' + str(run_col + 1) + ' ' + wall_type1 + '_' + wall_type2 + '.mpr', 'w')
        f.write(cnc.Woodwop().ww_open(Model.wall[run_col].height, Model.wall[run_col].depth, Model.furniture_thickness))
        f.write(cnc.Woodwop().ww_variables())

        if Model.wall[run_col].hasSockle:
            f.write(cnc.Woodwop().ww_variables_sockle())
            f.write(cnc.Woodwop().ww_milling_sockle())
        else:
            f.write(cnc.Woodwop().ww_milling())

        if run_col == 0:  # build first wall
            # f.write(cnc.Woodwop().ww_milling())
            f.write(cnc.Woodwop().ww_milling_backwall('R', Model.wall[run_col].reduced))  # send wall side (left/right)
            drilling_wall_btm(f, run_col, Model.wall[run_col].backwall, False)  # send file name, column, backwall info, drillings not mirrored == false
            if len(Model.wall[run_col].hasDoorLeft) > 0:
                drilling_wall_door(f, run_col, 'RIGHT')
            if len(Model.wall[run_col].hasDrawerStart) > 0:
                drilling_wall_drawer(f, run_col, False)
            if len(Model.wall[run_col].hasPushRight) > 0:
                drilling_wall_push_to_open(f, run_col, 'RIGHT')
            for run_shelf in range(1, Model.shelf_array[run_col]+1):  # ignore bottom board, ignore top board
                drilling_wall_mid(f, run_col, run_shelf, Model.wall[run_col].backwall, False)
            drilling_wall_top(f, run_col, Model.wall[run_col].backwall, False)

        if 0 < run_col < Model.columns:
            if Model.wall[run_col].backwall:
                f.write(cnc.Woodwop().ww_milling_backwall('R', Model.height_array[run_col]))  # from outside, so specifying milling length is required
            drilling_wall_btm(f, run_col, Model.wall[run_col].backwall, False)
            if len(Model.wall[run_col].hasDoorLeft) > 0:
                drilling_wall_door(f, run_col, 'RIGHT')
            if len(Model.wall[run_col].hasDrawerStart) > 0:
                drilling_wall_drawer(f, run_col, False)
            if len(Model.wall[run_col].hasPushRight) > 0:
                drilling_wall_push_to_open(f, run_col, 'RIGHT')
            for run_shelf in range(1, Model.shelf_array[run_col] + 1):  # ignore bottom board, ignore top board
                drilling_wall_mid(f, run_col, run_shelf, Model.wall[run_col].backwall, False)
            drilling_wall_top(f, run_col, Model.wall[run_col].backwall, False)

            # generate 2nd side
            f2 = open(Model.order_folder +'sciana/sciana_' + str(run_col + 1) + ' ' + wall_type1 + '_' + wall_type2 + '_2' + '.mpr', 'w')
            f2.write(cnc.Woodwop().ww_open(Model.wall[run_col].height, Model.wall[run_col].depth, Model.furniture_thickness))

            # f2.write(cnc.Woodwop().ww_variables())
            # if Model.wall[run_col].hasSockle:
            #     f2.write(cnc.Woodwop().ww_variables_sockle())
            #     f2.write(cnc.Woodwop().ww_milling_sockle(True))
            # else:
            #     f2.write(cnc.Woodwop().ww_milling())

            if Model.wall[run_col].backwall:
                f2.write(cnc.Woodwop().ww_variables())
                f2.write(cnc.Woodwop().ww_milling_backwall('L', Model.wall[run_col-1].reduced, '1'))  # from the inside, so no need to specify milling length
            drilling_wall_btm(f2, run_col, Model.wall[run_col].backwall, True)
            if len(Model.wall[run_col].hasDoorRight) > 0:
                drilling_wall_door(f2, run_col, 'LEFT')
            if len(Model.wall[run_col].hasDrawerEnd) > 0:
                drilling_wall_drawer(f2, run_col, True)
            if len(Model.wall[run_col].hasPushLeft) > 0:
                drilling_wall_push_to_open(f2, run_col, 'LEFT')
            for run_shelf in range(1, Model.shelf_array[run_col-1] + 1):  # ignore bottom board, ignore top board
                drilling_wall_mid(f2, run_col, run_shelf, Model.wall[run_col].backwall, True)
            drilling_wall_top(f2, run_col, Model.wall[run_col].backwall, True)
            f2.write(cnc.Woodwop().ww_close())
            f2.close()

        if run_col == Model.columns:
            # f.write(cnc.Woodwop().ww_milling())
            if Model.wall[run_col].backwall:
                f.write(cnc.Woodwop().ww_milling_backwall('L', Model.wall[run_col].reduced))  # from outside, so specifying milling length is not required
            drilling_wall_btm(f, run_col, Model.wall[run_col].backwall, True)
            if len(Model.wall[run_col].hasDoorRight) > 0:
                drilling_wall_door(f, run_col, 'LEFT')
            if len(Model.wall[run_col].hasDrawerEnd) > 0:
                drilling_wall_drawer(f, run_col, True)
            if len(Model.wall[run_col].hasPushLeft) > 0:
                drilling_wall_push_to_open(f, run_col, 'LEFT')
            for run_shelf in range(1, Model.shelf_array[run_col-1] + 1):  # ignore bottom board, ignore top board
                drilling_wall_mid(f, run_col, run_shelf, Model.wall[run_col].backwall, True)
            drilling_wall_top(f, run_col, Model.wall[run_col].backwall, True)

        f.write(cnc.Woodwop().ww_close())
        f.close()


def generate_mid():
    for run_col in range(Model.columns):
        count_BN = 0
        count_BD = 0
        for run_shelf in range(1, Model.shelf_array[run_col]+1):
            if Model.board[run_col][run_shelf].recess == False:
                boardtype = 'BD'  # full depth shelf
            else:
                boardtype = 'BN'  # recessed shelf

            has_dividerOnTop = True if  len(Model.board[run_col][run_shelf].hasDividerOnTop) > 0 else False
            has_dividerOnBottom = True if len(Model.board[run_col][run_shelf].hasDividerOnBottom) > 0 else False
            has_flapOnTop = True if Model.board[run_col][run_shelf].hasFlapOnTop else False
            has_flapBottom = True if Model.board[run_col][run_shelf].hasFlapOnBottom else False

            if has_dividerOnTop or has_dividerOnBottom or has_flapOnTop or has_flapBottom:
                board_number = '-'+str(run_shelf)
                multiplier = ''
            else:
                board_number = ''
                if boardtype == 'BN':
                    fix_depth = Model.board[run_col][run_shelf].depth
                    count_BN += 1
                    multiplier = str(count_BN) + 'x '
                    old_value = str(count_BN-1) + 'x '
                    if count_BN > 1:
                        os.rename(Model.order_folder+'polka/'+old_value+str(boardtype)+str(run_col + 1)+'.mpr', Model.order_folder+'polka/'+multiplier+str(boardtype)+str(run_col + 1)+'.mpr')
                        continue

                elif boardtype == 'BD':
                    fix_depth = Model.board[run_col][run_shelf].depth - Mid.fix_depth
                    count_BD += 1
                    multiplier = str(count_BD) + 'x '
                    old_value = str(count_BD-1) + 'x '
                    if count_BD > 1:
                        os.rename(Model.order_folder+'polka/'+old_value+str(boardtype)+str(run_col + 1)+'.mpr', Model.order_folder+'polka/'+multiplier+str(boardtype)+str(run_col + 1)+'.mpr')
                        continue

            f = open(Model.order_folder+'polka/'+multiplier+boardtype+str(run_col + 1) + board_number + '.mpr', 'w')
            f.write(cnc.Woodwop().ww_open(Model.board[run_col][run_shelf].width, fix_depth, Model.board[run_col][run_shelf].thickness))
            f.write(cnc.Woodwop().ww_variables())
            f.write(cnc.Woodwop().ww_milling())

            if Model.depth_array[run_col] > G.board_support:  # for bigger depths use more support, same in wall and btm board
                f.write(cnc.Woodwop().ww_drilling(Mid.x, Mid.y, Mid.diameter, Mid.depth))
                f.write(cnc.Woodwop().ww_drilling(Mid.x, 'y/2', Mid.diameter, Mid.depth))
                f.write(cnc.Woodwop().ww_drilling(Mid.x, ('y-' + str(Mid.y)), Mid.diameter, Mid.depth))
                f.write(cnc.Woodwop().ww_drilling(('x-' + str(Mid.x)), Mid.y, Mid.diameter, Mid.depth))
                f.write(cnc.Woodwop().ww_drilling(('x-' + str(Mid.x)), 'y/2', Mid.diameter, Mid.depth))
                f.write(cnc.Woodwop().ww_drilling(('x-' + str(Mid.x)), ('y-' + str(Mid.y)), Mid.diameter, Mid.depth))
            else:
                f.write(cnc.Woodwop().ww_drilling(Mid.x, Mid.y, Mid.diameter, Mid.depth))
                f.write(cnc.Woodwop().ww_drilling(Mid.x, ('y-' + str(Mid.y)), Mid.diameter, Mid.depth))
                f.write(cnc.Woodwop().ww_drilling(('x-' + str(Mid.x)), Mid.y, Mid.diameter, Mid.depth))
                f.write(cnc.Woodwop().ww_drilling(('x-' + str(Mid.x)), ('y-' + str(Mid.y)), Mid.diameter, Mid.depth))

            if has_dividerOnBottom:  # check if board has divider
                index = Model.board[run_col][run_shelf].hasDividerOnBottom[0]  # find this divider, check how much its recessed
                get_recess = Model.divider[index].get_recess_top  # get recess
                set_mid_x = 'x/2+' + str(Model.furniture_thickness / 2 - Common.z0)
                f.write(cnc.Woodwop().ww_drilling(set_mid_x, 'y-' + str(Divider.y_cam), Common.diameter_pin, Common.depth_pin_inserted))
                f.write(cnc.Woodwop().ww_drilling(set_mid_x, 'y-' + str(Divider.y_dowel), Common.diameter_dowel, Common.depth_dowel_inserted))
                f.write(cnc.Woodwop().ww_drilling(set_mid_x, get_recess + Divider.y_dowel, Common.diameter_dowel, Common.depth_dowel_inserted))
                f.write(cnc.Woodwop().ww_drilling(set_mid_x, get_recess + Divider.y_cam, Common.diameter_pin, Common.depth_pin_inserted))

            if has_flapOnTop or has_dividerOnTop:
                f2 = open('polka/' + boardtype + str(run_col + 1) + board_number + '_DRUGA_STRONA.mpr', 'w')
                f2.write(cnc.Woodwop().ww_open(Model.board[run_col][run_shelf].width, Model.board[run_col][run_shelf].depth, Model.board[run_col][run_shelf].thickness, 0, 0))
                f2.write(cnc.Woodwop().ww_variables())

                if has_flapOnTop:
                    f2.write(cnc.Woodwop().ww_mill_hole(Door.flap_hinge_wall_x, 'y-' + str(Door.flap_hinge_board_y), Door.flap_hinge_diameter, Door.flap_hinge_depth))
                    f2.write(cnc.Woodwop().ww_mill_hole('x-'+str(Door.flap_hinge_wall_x), 'y-' + str(Door.flap_hinge_board_y), Door.flap_hinge_diameter, Door.flap_hinge_depth, 2))

                if has_dividerOnTop:
                    index = Model.board[run_col][run_shelf].hasDividerOnTop[0]  # find this divider, check how much its recessed
                    get_recess = Model.divider[index].get_recess_bot  # get recess
                    set_mid_x = 'x/2+'+str(Model.furniture_thickness/2-Common.z0)
                    f2.write(cnc.Woodwop().ww_drilling(set_mid_x, 'y-' + str(get_recess + Divider.y_cam), Common.diameter_pin, Common.depth_pin_inserted))
                    f2.write(cnc.Woodwop().ww_drilling(set_mid_x, 'y-' + str(get_recess + Divider.y_dowel), Common.diameter_dowel, Common.depth_dowel_inserted))
                    f2.write(cnc.Woodwop().ww_drilling(set_mid_x, Divider.y_dowel, Common.diameter_dowel, Common.depth_dowel_inserted))
                    f2.write(cnc.Woodwop().ww_drilling(set_mid_x, Divider.y_cam, Common.diameter_pin, Common.depth_pin_inserted))
                f2.write(cnc.Woodwop().ww_close())
                f2.close()

            f.write(cnc.Woodwop().ww_close())
            f.close()


def generate_btm():
    for run_col in range(Model.columns):
        f = open(Model.order_folder+'dno/dno_' + str(run_col + 1) + '.mpr', 'w')
        fix_depth = Model.board[run_col][0].depth - Btm.fix_depth
        f.write(cnc.Woodwop().ww_open(Model.board[run_col][0].width, fix_depth, Model.board[run_col][0].thickness))
        f.write(cnc.Woodwop().ww_milling())
        f.write(cnc.Woodwop().ww_variables())

        if Model.depth_array[run_col] > G.board_support:  # for bigger depths use more support
            f.write(cnc.Woodwop().ww_drilling(Btm.x, Btm.y, Btm.diameter, Btm.depth))
            f.write(cnc.Woodwop().ww_drilling(Btm.x, 'y/2', Btm.diameter, Btm.depth))
            f.write(cnc.Woodwop().ww_drilling(Btm.x, ('y-' + str(Btm.y)), Btm.diameter, Btm.depth))
            f.write(cnc.Woodwop().ww_drilling(('x-' + str(Btm.x)), Btm.y, Btm.diameter, Btm.depth))
            f.write(cnc.Woodwop().ww_drilling(('x-' + str(Btm.x)), 'y/2', Btm.diameter, Btm.depth))
            f.write(cnc.Woodwop().ww_drilling(('x-' + str(Btm.x)), ('y-' + str(Btm.y)), Btm.diameter, Btm.depth))
        else:
            f.write(cnc.Woodwop().ww_drilling(Btm.x, Btm.y, Btm.diameter, Btm.depth))
            f.write(cnc.Woodwop().ww_drilling(Btm.x, ('y-' + str(Btm.y)), Btm.diameter, Btm.depth))
            f.write(cnc.Woodwop().ww_drilling(('x-' + str(Btm.x)), Btm.y, Btm.diameter, Btm.depth))
            f.write(cnc.Woodwop().ww_drilling(('x-' + str(Btm.x)), ('y-' + str(Btm.y)), Btm.diameter, Btm.depth))

        if Model.board[run_col][0].hasFlapOnTop or len(Model.board[run_col][0].hasDividerOnTop) > 0:
            f2 = open('dno/dno_' + str(run_col + 1)+'_2.mpr', 'w')
            f2.write(cnc.Woodwop().ww_open(Model.board[run_col][0].width, Model.board[run_col][0].depth, Model.board[run_col][0].thickness, 0, 0))
            f2.write(cnc.Woodwop().ww_variables())

            if Model.board[run_col][0].hasFlapOnTop:
                f2.write(cnc.Woodwop().ww_mill_hole(Door.flap_hinge_wall_x, 'y-' + str(Door.flap_hinge_board_y), Door.flap_hinge_diameter, Door.flap_hinge_depth))
                f2.write(cnc.Woodwop().ww_mill_hole('x-' + str(Door.flap_hinge_wall_x), 'y-' + str(Door.flap_hinge_board_y), Door.flap_hinge_diameter, Door.flap_hinge_depth, 2))

            if len(Model.board[run_col][0].hasDividerOnTop) > 0:
                set_mid_x = 'x/2+' + str(Model.furniture_thickness / 2 - Common.z0)
                f2.write(cnc.Woodwop().ww_drilling(set_mid_x, 'y-' + str(Divider.recess_extended + Divider.y_cam), Common.diameter_pin, Common.depth_pin_inserted))
                f2.write(cnc.Woodwop().ww_drilling(set_mid_x, 'y-' + str(Divider.recess_extended + Divider.y_dowel), Common.diameter_dowel, Common.depth_dowel_inserted))
                f2.write(cnc.Woodwop().ww_drilling(set_mid_x, Divider.y_dowel, Common.diameter_dowel, Common.depth_dowel_inserted))
                f2.write(cnc.Woodwop().ww_drilling(set_mid_x, Divider.y_cam, Common.diameter_pin, Common.depth_pin_inserted))
            f2.write(cnc.Woodwop().ww_close())
            f2.close()

        if Model.sockle_height > 0:
            for drill_sockle in Model.board[run_col][0].hasSockle:
                f.write(cnc.Woodwop().ww_drilling(drill_sockle, Sock.y, Sock.diameter, Sock.depth))
                f.write(cnc.Woodwop().ww_drilling(drill_sockle, Sock.y + Sock.raster, Sock.diameter, Sock.depth))
        f.write(cnc.Woodwop().ww_close())
        f.close()


def generate_top():
    for run_tabletop in range(len(Model.tabletop)):
        f = open(Model.order_folder+'blat/blat_' + str(run_tabletop + 1) + '.mpr', 'w')
        f.write(cnc.Woodwop().ww_open(Model.tabletop[run_tabletop].width, Model.tabletop[run_tabletop].depth, Model.tabletop[run_tabletop].thickness))
        f.write(cnc.Woodwop().ww_milling())
        f.write(cnc.Woodwop().ww_variables())

        if Model.tabletop[run_tabletop].cover == 'LEFT':
            f.write(cnc.Woodwop().ww_milling_backwall('R', 'TABLETOP-RIGHT'))
        elif Model.tabletop[run_tabletop].cover == 'RIGHT':
            f.write(cnc.Woodwop().ww_milling_backwall('R', 'TABLETOP-LEFT'))
        elif Model.tabletop[run_tabletop].cover == 'BOTH':
            f.write(cnc.Woodwop().ww_milling_backwall('R', 'TABLETOP-BOTH'))

        # RIGHT SIDE IN WOODWOP
        if Model.tabletop[run_tabletop].cover == 'LEFT' or Model.tabletop[run_tabletop].cover == 'BOTH':
            start_tabletop = Model.wall[Model.tabletop[run_tabletop].start].x - Model.furniture_thickness/2   # relevant if worktop is covering some walls
            f.write(cnc.Woodwop().ww_drilling('x-'+str(Common.z1_inserted), Top.y, Common.diameter_pin, Common.depth_pin_inserted))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(Common.z1_inserted), Top.y_dowel, Common.diameter_dowel, Common.depth_dowel_inserted))
            if Model.depth_array[Model.tabletop[run_tabletop].start-1] > G.board_support:
                f.write(cnc.Woodwop().ww_drilling('x-'+str(Common.z1_inserted), 'y/2', Common.diameter_dowel, Common.depth_dowel_inserted))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(Common.z1_inserted), 'y-'+str(Top.y), Common.diameter_pin, Common.depth_pin_inserted))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(Common.z1_inserted), 'y-'+str(Top.y_dowel), Common.diameter_dowel, Common.depth_dowel_inserted))
        else:
            f.write(cnc.Woodwop().ww_drilling('x-' + str(Mid.x), Mid.y, Mid.diameter, Mid.depth))
            if Model.depth_array[Model.tabletop[run_tabletop].start-1] > G.board_support:
                f.write(cnc.Woodwop().ww_drilling('x-' + str(Mid.x), 'y/2', Mid.diameter, Mid.depth))
            f.write(cnc.Woodwop().ww_drilling('x-' + str(Mid.x), 'y-'+str(Mid.y), Mid.diameter, Mid.depth))

        # WORKTOP COVERING A WALL
        for covered in range(Model.tabletop[run_tabletop].start+1, Model.tabletop[run_tabletop].end):
            covered_tabletop = Model.wall[covered].x
            distance = covered_tabletop - start_tabletop  # distance to the middle of covered wall, from the first edge of tabletop
            position_x = distance + Model.furniture_thickness/2 - Common.z0  # distance to the drill
            f.write(cnc.Woodwop().ww_drilling('x-'+str(position_x), Top.y, Common.diameter_pin, Common.depth_pin_inserted))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(position_x), Top.y_dowel, Common.diameter_dowel, Common.depth_dowel_inserted))
            if Model.depth_array[Model.tabletop[run_tabletop].start-1] > G.board_support:
                f.write(cnc.Woodwop().ww_drilling('x-'+str(position_x), 'y/2', Common.diameter_dowel, Common.depth_dowel_inserted))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(position_x), 'y-'+str(Top.y), Common.diameter_pin, Common.depth_pin_inserted))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(position_x), 'y-'+str(Top.y_dowel), Common.diameter_dowel, Common.depth_dowel_inserted))

        # LEFT SIDE IN WOODWOP (for example: last wall is covered right)
        if Model.tabletop[run_tabletop].cover == 'RIGHT' or Model.tabletop[run_tabletop].cover == 'BOTH':
            f.write(cnc.Woodwop().ww_drilling(Common.z1_inserted, Top.y, Common.diameter_pin, Common.depth_pin_inserted))
            f.write(cnc.Woodwop().ww_drilling(Common.z1_inserted, Top.y_dowel, Common.diameter_dowel, Common.depth_dowel_inserted))
            if Model.depth_array[Model.tabletop[run_tabletop].start-1] > G.board_support:
                f.write(cnc.Woodwop().ww_drilling(Common.z1_inserted, 'y/2', Common.diameter_dowel, Common.depth_dowel_inserted))
            f.write(cnc.Woodwop().ww_drilling(Common.z1_inserted, 'y-'+str(Top.y), Common.diameter_pin, Common.depth_pin_inserted))
            f.write(cnc.Woodwop().ww_drilling(Common.z1_inserted, 'y-'+str(Top.y_dowel), Common.diameter_dowel, Common.depth_dowel_inserted))
        else:
            f.write(cnc.Woodwop().ww_drilling(Mid.x, Mid.y, Mid.diameter, Mid.depth))
            if Model.depth_array[Model.tabletop[run_tabletop].start-1] > G.board_support:
                f.write(cnc.Woodwop().ww_drilling(Mid.x, 'y/2', Mid.diameter, Mid.depth))
            f.write(cnc.Woodwop().ww_drilling(Mid.x, 'y-'+str(Mid.y), Mid.diameter, Mid.depth))

        if len(Model.tabletop[run_tabletop].hasDivider) > 0:
            if Model.tabletop[run_tabletop].cover == 'LEFT' or Model.tabletop[run_tabletop].cover == 'RIGHT' or Model.tabletop[run_tabletop].cover == 'BOTH':
                backwall_recess = G.backwall
            else:
                backwall_recess = 0

            for each_divider in range(0, len(Model.tabletop[run_tabletop].hasDivider), 2):
                get_mid_x = Model.tabletop[run_tabletop].hasDivider[each_divider+1] + Model.furniture_thickness/2 - Common.z0  # get middle divider position, fix for z
                f.write(cnc.Woodwop().ww_drilling(get_mid_x, 'y-' + str(backwall_recess + Divider.y_cam), Common.diameter_pin, Common.depth_pin_inserted))
                f.write(cnc.Woodwop().ww_drilling(get_mid_x, 'y-' + str(backwall_recess + Divider.y_dowel), Common.diameter_dowel, Common.depth_dowel_inserted))
                f.write(cnc.Woodwop().ww_drilling(get_mid_x, Divider.recess_extended + Divider.y_dowel, Common.diameter_dowel, Common.depth_dowel_inserted))
                f.write(cnc.Woodwop().ww_drilling(get_mid_x, Divider.recess_extended + Divider.y_cam, Common.diameter_pin, Common.depth_pin_inserted))

        f.write(cnc.Woodwop().ww_close())
        f.close()


def generate_door():
    for run_door in range(len(Model.door)):
        if Model.door[run_door].doortype == 'door':
            if Model.door[run_door].open == 'right':
                door_type = '_PRAWE'
            elif Model.door[run_door].open == 'left':
                door_type = '_LEWE'

            f = open(Model.order_folder+'drzwi/drzwi_' + str(run_door) + door_type +'.mpr', 'w')
            f.write(cnc.Woodwop().ww_open(Model.door[run_door].height, Model.door[run_door].width, Model.door[run_door].thickness))
            f.write(cnc.Woodwop().ww_variables())
            f.write(cnc.Woodwop().ww_milling())

            for cup_position in Model.door[run_door].hinges:
                if Model.door[run_door].open == 'right':
                    f.write(cnc.Woodwop().ww_drilling('x-' + str(cup_position), 'y-'+str(Door.hinge_y_cup), Door.hinge_diameter_cup, Door.hinge_depth_cup))
                    f.write(cnc.Woodwop().ww_drilling('x-' + str(cup_position + Door.hinge_raster_screw_door / 2), 'y-'+str(Door.hinge_y_screw), Door.hinge_diameter_screw, Door.hinge_depth_screw))
                    f.write(cnc.Woodwop().ww_drilling('x-' + str(cup_position - Door.hinge_raster_screw_door / 2), 'y-'+str(Door.hinge_y_screw), Door.hinge_diameter_screw, Door.hinge_depth_screw))
                    # f.write(cnc.Woodwop().ww_drilling('x-' + str(Model.door[run_door].pushToOpen), Door.push_y, Door.push_diameter, Door.push_depth))
                elif Model.door[run_door].open == 'left':
                    f.write(cnc.Woodwop().ww_drilling('x-' + str(cup_position), Door.hinge_y_cup, Door.hinge_diameter_cup, Door.hinge_depth_cup))
                    f.write(cnc.Woodwop().ww_drilling('x-' + str(cup_position + Door.hinge_raster_screw_door / 2), Door.hinge_y_screw, Door.hinge_diameter_screw, Door.hinge_depth_screw))
                    f.write(cnc.Woodwop().ww_drilling('x-' + str(cup_position - Door.hinge_raster_screw_door / 2), Door.hinge_y_screw, Door.hinge_diameter_screw, Door.hinge_depth_screw))
                    # f.write(cnc.Woodwop().ww_drilling('x-' + str(Model.door[run_door].pushToOpen), 'y-'+str(Door.push_y), Door.push_diameter, Door.push_depth))

            f.write(cnc.Woodwop().ww_close())
            f.close()
        elif Model.door[run_door].doortype == 'drawer':
            f = open(Model.order_folder+'szuflada/czolo' + str(run_door) + '.mpr', 'w')
            f.write(cnc.Woodwop().ww_open(Model.door[run_door].height, Model.door[run_door].width, Model.door[run_door].thickness))
            f.write(cnc.Woodwop().ww_variables())
            f.write(cnc.Woodwop().ww_milling())
            f.write(cnc.Woodwop().ww_close())
            f.close()

            f = open(Model.order_folder+'szuflada/bok' + str(run_door) + '.mpr', 'w')
            drilling_drawer_z = Drawer.thickness/2+0.1
            cam_y = Drawer.bottom_fix + Model.door[run_door].drawer_front_height/2
            dowel_1_y = Drawer.bottom_fix + Drawer.dowel_distance_1
            dowel_2_y = Drawer.bottom_fix + Model.door[run_door].drawer_front_height + Drawer.front_lowered - Drawer.dowel_distance_1

            f.write(cnc.Woodwop().ww_open(Model.door[run_door].drawer_side_depth, Model.door[run_door].drawer_side_height, Drawer.thickness))
            f.write(cnc.Woodwop().ww_variables())
            f.write(cnc.Woodwop().ww_milling())
            f.write(cnc.Woodwop().ww_sawing())
            f.write(cnc.Woodwop().ww_drilling(drilling_drawer_z, dowel_1_y, Common.diameter_dowel, Common.depth_dowel_inserted))
            f.write(cnc.Woodwop().ww_drilling(drilling_drawer_z, cam_y, Common.diameter_pin, Common.depth_pin_inserted))
            f.write(cnc.Woodwop().ww_drilling(drilling_drawer_z, dowel_2_y, Common.diameter_dowel, Common.depth_dowel_inserted))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(drilling_drawer_z), dowel_1_y, Common.diameter_dowel, Common.depth_dowel_inserted))
            f.write(cnc.Woodwop().ww_drilling('x-' + str(drilling_drawer_z), cam_y, Common.diameter_pin, Common.depth_pin_inserted))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(drilling_drawer_z), dowel_2_y, Common.diameter_dowel, Common.depth_dowel_inserted))
            f.write(cnc.Woodwop().ww_close())
            f.close()

            f = open(Model.order_folder+'szuflada/przod' + str(run_door) + '.mpr', 'w')
            f.write(cnc.Woodwop().ww_open(Model.door[run_door].drawer_front_width, Model.door[run_door].drawer_front_height, Drawer.thickness))
            f.write(cnc.Woodwop().ww_variables())
            f.write(cnc.Woodwop().ww_milling())
            f.write(cnc.Woodwop().ww_horizontal_drilling(0, Drawer.dowel_distance_1, Drawer.front_z, Common.diameter_dowel, Common.depth_dowel))
            f.write(cnc.Woodwop().ww_horizontal_drilling(0, Model.door[run_door].drawer_front_height/2, Drawer.front_z, Common.diameter_pin, Common.depth_pin))
            f.write(cnc.Woodwop().ww_drilling(Common.x_cam, Model.door[run_door].drawer_front_height/2, Common.diameter_cam, Common.depth_cam))
            f.write(cnc.Woodwop().ww_horizontal_drilling(0, 'y-'+str(Drawer.dowel_distance_1), Drawer.front_z, Common.diameter_dowel, Common.depth_dowel))

            f.write(cnc.Woodwop().ww_horizontal_drilling('x', Drawer.dowel_distance_1, Drawer.front_z, Common.diameter_dowel, Common.depth_dowel, 'X-'))
            f.write(cnc.Woodwop().ww_horizontal_drilling('x', Model.door[run_door].drawer_front_height/2, Drawer.front_z, Common.diameter_pin, Common.depth_pin, 'X-'))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(Common.x_cam), Model.door[run_door].drawer_front_height/2, Common.diameter_cam, Common.depth_cam))
            f.write(cnc.Woodwop().ww_horizontal_drilling('x', 'y-'+str(Drawer.dowel_distance_1), Drawer.front_z, Common.diameter_dowel, Common.depth_dowel, 'X-'))
            f.write(cnc.Woodwop().ww_close())
            f.close()

            f = open(Model.order_folder+'szuflada/tyl' + str(run_door) + '.mpr', 'w')
            f.write(cnc.Woodwop().ww_open(Model.door[run_door].drawer_front_width, Model.door[run_door].drawer_front_height, Drawer.thickness))
            f.write(cnc.Woodwop().ww_variables())
            f.write(cnc.Woodwop().ww_milling())
            f.write(cnc.Woodwop().ww_horizontal_drilling(0, Drawer.dowel_distance_1, Drawer.front_z, Common.diameter_dowel, Common.depth_dowel))
            f.write(cnc.Woodwop().ww_horizontal_drilling(0, Model.door[run_door].drawer_front_height/2, Drawer.front_z, Common.diameter_pin, Common.depth_pin))
            f.write(cnc.Woodwop().ww_drilling(Common.x_cam, Model.door[run_door].drawer_front_height/2, Common.diameter_cam, Common.depth_cam))
            f.write(cnc.Woodwop().ww_horizontal_drilling(0, 'y-'+str(Drawer.dowel_distance_1), Drawer.front_z, Common.diameter_dowel, Common.depth_dowel))
            f.write(cnc.Woodwop().ww_drilling(Drawer.back_slider_x, Drawer.back_slider_y, Drawer.back_slider_diameter, Drawer.back_slider_depth))

            f.write(cnc.Woodwop().ww_horizontal_drilling('x', Drawer.dowel_distance_1, Drawer.front_z, Common.diameter_dowel, Common.depth_dowel, 'X-'))
            f.write(cnc.Woodwop().ww_horizontal_drilling('x', Model.door[run_door].drawer_front_height/2, Drawer.front_z, Common.diameter_pin, Common.depth_pin, 'X-'))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(Common.x_cam), Model.door[run_door].drawer_front_height/2, Common.diameter_cam, Common.depth_cam))
            f.write(cnc.Woodwop().ww_horizontal_drilling('x', 'y-'+str(Drawer.dowel_distance_1), Drawer.front_z, Common.diameter_dowel, Common.depth_dowel, 'X-'))
            f.write(cnc.Woodwop().ww_drilling('x-'+str(Drawer.back_slider_x), Drawer.back_slider_y, Drawer.back_slider_diameter, Drawer.back_slider_depth))
            f.write(cnc.Woodwop().ww_close())
            f.close()
        elif Model.door[run_door].doortype == 'flap':
            f = open(Model.order_folder+'drzwi/klapa_' + str(run_door) + '.mpr', 'w')
            f.write(cnc.Woodwop().ww_open(Model.door[run_door].width, Model.door[run_door].height, Model.door[run_door].thickness))
            f.write(cnc.Woodwop().ww_variables())
            f.write(cnc.Woodwop().ww_milling())
            for cup_position in Model.door[run_door].hinges:
                f.write(cnc.Woodwop().ww_mill_hole(cup_position, Door.flap_hinge_door_y, Door.flap_hinge_diameter, Door.flap_hinge_depth, 2))
                f.write(cnc.Woodwop().ww_mill_hole('x-' + str(cup_position), Door.flap_hinge_door_y, Door.flap_hinge_diameter, Door.flap_hinge_depth, 3))
            f.write(cnc.Woodwop().ww_close())
            f.close()


def generate_divider():
    for run_divider in range(len(Model.divider)):
        f = open(Model.order_folder+'pionik/pion_' + str(run_divider) + '.mpr', 'w')
        f.write(cnc.Woodwop().ww_open(Model.divider[run_divider].height, Model.divider[run_divider].depth, Model.divider[run_divider].thickness))
        f.write(cnc.Woodwop().ww_variables())
        f.write(cnc.Woodwop().ww_milling())
        f.write(cnc.Woodwop().ww_horizontal_drilling(0, Divider.y_cam, Common.z1, Common.diameter_pin, Common.depth_pin))
        f.write(cnc.Woodwop().ww_drilling(Common.x_cam, Divider.y_cam, Common.diameter_cam, Common.depth_cam))
        f.write(cnc.Woodwop().ww_horizontal_drilling(0, Divider.y_dowel, Common.z1, Common.diameter_dowel, Common.depth_dowel))
        f.write(cnc.Woodwop().ww_horizontal_drilling(0, 'y-' + str(Divider.y_dowel), Common.z1, Common.diameter_dowel, Common.depth_dowel))
        f.write(cnc.Woodwop().ww_drilling(Common.x_cam, 'y-' + str(Divider.y_cam), Common.diameter_cam, Common.depth_cam))
        f.write(cnc.Woodwop().ww_horizontal_drilling(0, 'y-' + str(Divider.y_cam), Common.z1, Common.diameter_pin, Common.depth_pin))

        f.write(cnc.Woodwop().ww_horizontal_drilling('x', Divider.y_cam, Common.z1, Common.diameter_pin, Common.depth_pin, 'X-'))
        f.write(cnc.Woodwop().ww_drilling('x-'+str(Common.x_cam), Divider.y_cam, Common.diameter_cam, Common.depth_cam))
        f.write(cnc.Woodwop().ww_horizontal_drilling('x', Divider.y_dowel, Common.z1, Common.diameter_dowel, Common.depth_dowel, 'X-'))
        f.write(cnc.Woodwop().ww_horizontal_drilling('x', 'y-' + str(Divider.y_dowel), Common.z1, Common.diameter_dowel, Common.depth_dowel, 'X-'))
        f.write(cnc.Woodwop().ww_drilling('x-'+str(Common.x_cam), 'y-' + str(Divider.y_cam), Common.diameter_cam, Common.depth_cam))
        f.write(cnc.Woodwop().ww_horizontal_drilling('x', 'y-' + str(Divider.y_cam), Common.z1, Common.diameter_pin, Common.depth_pin, 'X-'))

        f.write(cnc.Woodwop().ww_close())
        f.close()


def delete_folders():
    for folder in Model.folders:
        if os.path.exists(Model.order_folder+folder):  # check if folder exists
            shutil.rmtree(Model.order_folder+folder)  # delete folder
        os.makedirs(Model.order_folder+folder)  # create folder


def export_boards_to_excel():
    kwargs = {
        "furniture_thickness": Model.furniture_thickness,
        "texture": Model.active_texture,
        "backwall_texture": Model.active_backwall_texture,
        "wall": Model.wall,
        "board": Model.board,
        "columns": Model.columns,
        "shelf_array": Model.shelf_array,
        "door": Model.door,
        "sockle": Model.sockle,
        "divider": Model.divider,
        "tabletop": Model.tabletop,
        "order_id": Model.order_id,
        "order_folder": Model.order_folder
    }
    bom.excel_boards(**kwargs)


def get_accessories():
    def get_board_accs():
        for each in range(Model.columns):
            shelves_in_column = Model.shelf_array[each]
            if Model.depth_array[each] > G.board_support:
                additional_support = 2
            else:
                additional_support = 0
            acc.Used.brd['amount'] += ((4+additional_support) * shelves_in_column)
            acc.Used.wall_brd['amount'] += ((4+additional_support) * shelves_in_column)
    get_board_accs()

    def get_worktop_accs():
        for each in range(len(Model.tabletop)):
            if Model.depth_array[Model.tabletop[each].start] > G.board_support:
                additional_support = 2
            else:
                additional_support = 0
            if Model.tabletop[each].cover == 'BOTH':
                acc.Used.dowel['amount'] += 4 + additional_support
                acc.Used.pin['amount'] += 4
                acc.Used.cam['amount'] += 4
            elif Model.tabletop[each].cover == 'LEFT' or Model.tabletop[each].cover == 'RIGHT':
                acc.Used.dowel['amount'] += 2 + additional_support/2
                acc.Used.pin['amount'] += 2
                acc.Used.cam['amount'] += 2
                acc.Used.brd['amount'] += 2 + additional_support/2
                acc.Used.wall_brd['amount'] += 2 + additional_support/2
            elif Model.tabletop[each].cover == 'NONE':
                acc.Used.brd['amount'] += 4 + additional_support
                acc.Used.wall_brd['amount'] += 4 + additional_support
            else:
                print('unknown tabletop cover')
    get_worktop_accs()

    def btm_accs():
        for each in range(Model.columns):
            sockles_on_btm_board = len(Model.board[each][0].hasSockle)
            acc.Used.btm_sockle['amount'] += sockles_on_btm_board
            acc.Used.sockle['amount'] += sockles_on_btm_board

            if Model.depth_array[each] > G.board_support:
                additional_support = 2
            else:
                additional_support = 0
            acc.Used.btm['amount'] += 4+additional_support
            acc.Used.wall_btm['amount'] += 4+additional_support
    btm_accs()

    def door_accs():
        for each in range(len(Model.door)):
            if Model.door[each].doortype == 'door' or Model.door[each].doortype == 'doubleLEFT' or Model.door[each].doortype == 'doubleRIGHT':
                hinges_in_door = len(Model.door[each].hinges)
                if Model.furniture_thickness > 24:
                    acc.Used.door_hinge_straight['amount'] += hinges_in_door
                else:
                    acc.Used.door_hinge_110['amount'] += hinges_in_door
                acc.Used.door_plate['amount'] += hinges_in_door
                acc.Used.door_push['amount'] += 1
            elif Model.door[each].doortype == 'drawer':
                if Model.width_array[Model.door[each].column-1] > G.board_support:
                    acc.Used.drawer_slider_sync['amount'] += 1
                acc.Used.drawer_slider['length'] = Model.door[each].slider
                acc.Used.drawer_slider['amount'] += 1
                acc.Used.drawer_slider_push['amount'] += 1
            elif Model.door[each].doortype == 'flap':
                acc.Used.door_push['amount'] += 1
                acc.Used.door_arm_flap['amount'] += 2
                acc.Used.door_hinge_flap['amount'] += 2
            else:
                print('unknown door type')
    door_accs()

    def hanger_accs():
        for hanger in Model.hanger:
            if hanger.type == 'runner':
                acc.Used.hanger_runner['amount'] += 1
            elif hanger.type == 'tube':
                acc.Used.hanger_tube['amount'] += 1
            else:
                print('unknown hanger type')
    hanger_accs()

    def divider_accs():
        for divider in Model.divider:
            acc.Used.dowel['amount'] += 4
            acc.Used.pin['amount'] += 4
            acc.Used.cam['amount'] += 4
            print('check the number off added dowels, pins and cams in divider')
    divider_accs()

# calculations
load_objects()

# boards
export_boards_to_excel()
delete_folders()

# cnc
generate_walls()
generate_mid()
generate_btm()
generate_top()
generate_door()
generate_divider()

# accessories
get_accessories()
acc.excel_accs(Model.order_id, Model.order_folder)
