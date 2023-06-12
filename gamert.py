import lvgl as lv
from src import display_tools
from src import logic
from src import color_map as cm
import pyRTOS

# creates an empty matrix with an unique tile
mat = logic.start_game()
task_run = None

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# defines an event for pressing the button
def event_cb(evt):
    btn = evt.get_target() # pressed button
    btn_label = btn.get_child(0) # its label
    if btn_label is not None:
        text = btn_label.get_text()
        if text == "^":
            direction = UP
        elif text == "v":
            direction = DOWN
        elif text == "<":
            direction = LEFT
        else:
            direction = RIGHT

    global task_run
    task_run.notify_set_value(index=0, state=1, value=direction)
    print(f"Send {direction}")

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
    ## Setup code
    global mat

    ##
    yield

    while True:
        self.wait_for_notification(index=0, state=1)
        direction = self.notify_get_value(index=0)
        if direction != 0:
            print("Run")
            self.notify_set_value(index=0, value=0)
            # we have to move up
            if(direction == UP):
                # call the move_up function
                mat, flag = logic.move_up(mat)

            # the above process will be followed for type of move

            # to move down
            elif(direction == DOWN):
                mat, flag = logic.move_down(mat)

            # to move left
            elif(direction == LEFT):
                mat, flag = logic.move_left(mat)

            # to move right
            elif(direction == RIGHT):
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

        yield [pyRTOS.timeout(0.1)]

def grid_update(self):
    print("Update - setup")
    ## Setup code
    global cont
    global mat
    colors = cm.color_map
    ## End setup code
    yield

    while True:
        print("Update")
        # change the matrix after each move.
        for i in range (4):
            for j in range(4):
                pos = 4*i+j
                tile = cont.get_child(pos)
                tile.set_style_bg_color(lv.color_hex(colors[str(mat[i][j])]), 0)
                
                label = tile.get_child(0)
                if(mat[i][j] == 0):
                    label.set_text(' ')
                elif(mat[i]):
                    label.set_text(str(mat[i][j]))
        yield [pyRTOS.timeout(0.1)]

def main():
    d = display_tools.get_display()

    import lv_utils
    if not lv_utils.event_loop.is_running():
        lv_utils.event_loop()
    
    load_scr()
    global task_run
    task_run = pyRTOS.Task(run, priority=1, name="run", notifications=1)
    pyRTOS.add_task(task_run)
    pyRTOS.add_task(pyRTOS.Task(grid_update, priority=2, name="update"))
    
    pyRTOS.start()

if __name__ == '__main__':
    main()
