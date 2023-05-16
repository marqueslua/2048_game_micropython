import lvgl as lv
from lab import display_tools

#ball = lv.led(lv.scr_act())

def event_cb(evt):
    cont = lv.obj(lv.scr_act())
    cont.align(lv.ALIGN.CENTER,0,-40)
    cont.set_size(200, 200)
    #code = evt.get_code() # código do evento (lv.EVENT.CLICKED)
    obj = evt.get_target()
    btn_label = obj.get_child(0)
    if btn_label is not None:
        ball = lv.led(cont)
        ball.align(lv.ALIGN.CENTER,0,0)
        ball.off()
        bx, by = ball.get_x(), ball.get_y()
        text = btn_label.get_text()
        if text == "^":
            by = by - 10
        elif text == "v":
            by = by + 10
        elif text == "<":
            bx = bx - 10
        else:
            bx = bx + 10

        ball.set_pos(bx,by)

def create_button(lbl, dx, dy):
    bt = lv.btn(lv.scr_act())
    bt.align(lv.ALIGN.BOTTOM_MID,dx,dy)
    bt.set_size(30,30)
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
    up = create_button("^", 0, -50)
    down = create_button("v", 0, -10)
    left = create_button("<", -40, -10)
    right = create_button(">", 40, -10)

    #print(dir(lv.btn)) # -> shows all attributes and functions of a type

    #cont = lv.obj(lv.scr_act())
    #cont.align(lv.ALIGN.CENTER,0,-40)
    #cont.set_size(200, 200)

    #global ball
    #ball.align(lv.ALIGN.CENTER,0,-40)
    #ball.off()


def main():
    d = display_tools.get_display()

    import lv_utils
    if not lv_utils.event_loop.is_running():
        lv_utils.event_loop()
    
    load_scr()

if __name__ == '__main__':
    main()