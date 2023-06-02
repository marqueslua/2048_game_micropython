import lvgl as lv
from src import display_tools
from src import logic
from src import color_map as cm
import pyRTOS

# creates an empty matrix with an unique tile
mat = logic.start_game()

# defines an event for pressing the button
def event_cb(evt):
    btn = evt.get_target() # pressed button
    btn_label = btn.get_child(0) # its label
    if btn_label is not None:
        text = btn_label.get_text()
        if text == "^":
            direction = 0
        elif text == "v":
            direction = 1
        elif text == "<":
            direction = 2
        else:
            direction = 3
    runtsk.notify_set_value(index=0, state=1, value=direction)

def create_button(lbl, dx, dy):
    bt = lv.btn(lv.scr_act())
    bt.align(lv.ALIGN.BOTTOM_MID,dx,dy-10)
    bt.set_size(30,30)
    # button text
    label=lv.label(bt)
    label.set_text(lbl)
    label.center()
    # set event
    bt.add_event_cb(event_cb, lv.EVENT.CLICKED, None)
    return bt

def load_scr():
    scr = lv.scr_act()
    lv.scr_load(scr)
    scr.set_style_bg_color(lv.color_hex(0x003a57), lv.PART.MAIN)

    # create buttons
    up = create_button("^", 0, -40)
    down = create_button("v", 0, 0)
    left = create_button("<", -40, 0)
    right = create_button(">", 40, 0)

    # create global container
    global cont
    cont = lv.obj(lv.scr_act())
    cont.align(lv.ALIGN.CENTER,0,-40)
    cont.set_size(220, 220)
    cont.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
    cont.set_style_pad_row(5, 0)
    cont.set_style_pad_column(5, 0)

    # create spaces for the 16 tiles
    for i in range(16):
        obj = lv.obj(cont)
        obj.set_size(43, 43)
        obj.clear_flag(lv.obj.FLAG.SCROLLABLE)
        label = lv.label(obj)
        label.set_text(' ')
        label.center()

# run a command up, down, left or right
def run(self):
    global mat
    try:
        direction = self.notify_get_value(index=0)
        # we have to move up
        if(direction == 0):
            # call the move_up function
            mat, flag = logic.move_up(mat)
    
        # the above process will be followed
        # in case of each type of move
        # below
    
        # to move down
        elif(direction == 1):
            mat, flag = logic.move_down(mat)
    
        # to move left
        elif(direction == 2):
            mat, flag = logic.move_left(mat)
    
        # to move right
        elif(direction == 2):
            mat, flag = logic.move_right(mat)

        # get the current status
        status = logic.get_current_state(mat)
        if(status == 'GAME NOT OVER'):
            logic.add_new_2(mat)
        #elif(status == 'WON'):
        #    global cont
        #    text = lv.label(cont)
        #    text.set_text('YOU WON')
        #    text.center()
        #if(status == 'LOST'):
        #    global cont
        #    text = lv.label(cont)
        #    text.set_text('GAME OVER')
        #    text.center()
            
        # change the matrix after each move.
        for i in range (4):
            for j in range(4):
                global cont
                pos = 4*i+j
                tile = cont.get_child(pos)
                label = tile.get_child(0)
                tile.set_style_bg_color(lv.color_hex(cm.color_map[str(mat[i][j])]), 0)
                if(mat[i][j] == 0):
                    label.set_text(' ')
                elif(mat[i]):
                    label.set_text(str(mat[i][j]))

    except Exception as e:
        pass

    yield [pyRTOS.timeout(0.100)]

#def grid_update(self):
#    
#    yield [pyRTOS.timeout(0.100)]

runtsk = pyRTOS.Task(run, priority=1, name="run", notifications=1)

def main():
    d = display_tools.get_display()

    import lv_utils
    if not lv_utils.event_loop.is_running():
        lv_utils.event_loop()
    
    load_scr()
    global runtsk
    pyRTOS.add_task(runtsk)
    #pyRTOS.add_task(pyRTOS.Task(grid_update, priority=2, name="update"))
    
    pyRTOS.start()

if __name__ == '__main__':
    main()
