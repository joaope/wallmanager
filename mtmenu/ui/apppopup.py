from pymt import *
from threading import Timer
from config import APPPOPUP_SIZE, MAINWINDOW_SIZE, APPSLIST_POPUP_DURATION
from utils import get_trimmed_label_widget

class AppPopup(MTWidget):

    def __init__(self, app, touch_pos, app_button, **kwargs):
        kwargs.setdefault('size', APPPOPUP_SIZE)
        
        # Calculate popup position relative to touch
        # Up-left corner on touch position
        pos_x, pos_y = touch_pos[0], touch_pos[1] - APPPOPUP_SIZE[1]
        
        # Avoid popup from being partially hidden
        if pos_x+APPPOPUP_SIZE[0] > MAINWINDOW_SIZE[0]: # check right
            pos_x = MAINWINDOW_SIZE[0] - APPPOPUP_SIZE[0] - 10
        
        if pos_y < 0: # check bottom
            pos_y = 10
            
        kwargs.setdefault('pos', (pos_x, pos_y))
        super(AppPopup, self).__init__(**kwargs)

        self.app = app
        self.app_button = app_button     
        self.timer = Timer(APPSLIST_POPUP_DURATION, self.close)
        self.timer.start()
        
        self.play_btn_pos = ()
        self.cancel_btn_pos = ()
        self.btns_size = ()
        
        self.label_app_name_text = self.app.name
        self.label_app_category_text = 'Category: %s' % self.app.category
        self.label_app_owner_text = 'Owner: %s' % self.app.owner
        self.label_app_runs_text = 'Runs: %s' % self.app.runs
        self.label_app_updated_text = 'Last Updated: %s' % self.app.date_updated


    def draw(self):
        
        x,y = list(self.pos)
        a,b = list(self.size)
        margin = 20
        max_label_width = a - margin*2
        
        # Background
        drawRoundedRectangle(pos = self.pos,
                     radius = 10,
                     size = self.size,
                     precision = 0.3, 
                     color = (0,0,0,0.9))
        
        # Title
        label_obj, self.label_app_name_text = get_trimmed_label_widget(text = self.label_app_name_text,
                                                                       position = (x + margin, y + b - 50),
                                                                       font_size = 20,
                                                                       max_width = max_label_width)
        label_obj.draw()
        
        # Category
        label_obj, self.label_app_category_text = get_trimmed_label_widget(text = self.label_app_category_text,
                                                                           position = (x + margin, y + b - 90),
                                                                           font_size = 15,
                                                                           max_width = max_label_width)
        label_obj.draw()
        
        # Owner
        label_obj, self.label_app_owner_text = get_trimmed_label_widget(text = self.label_app_owner_text,
                                                                        position = (x + margin, y + b - 115),
                                                                        font_size = 15,
                                                                        max_width = max_label_width)
        label_obj.draw()
        
        # Runs
        label_obj, self.label_app_runs_text = get_trimmed_label_widget(text = self.label_app_runs_text,
                                                                       position = (x + margin, y + b - 140),
                                                                       font_size = 15,
                                                                       max_width = max_label_width)
        label_obj.draw()
        
        # Last Updated
        label_obj, self.label_app_updated_text = get_trimmed_label_widget(text = self.label_app_updated_text,
                                                                          position = (x + margin, y + b - 165),
                                                                          font_size = 15,
                                                                          max_width = max_label_width)
        label_obj.draw()
        
        # Buttons
        buttons_size = (self.size[0]/2 - margin - 2, 45)
        button_play_pos = (x+margin, y+margin)
        button_close_pos = (x+margin+buttons_size[0] + 4, y+margin)
        
        self.btns_size = buttons_size
        self.play_btn_pos = button_play_pos
        self.close_btn_pos = button_close_pos
        
        # Play
        drawRoundedRectangle(pos = button_play_pos,
                             radius = 8,
                             size = buttons_size,
                             precision = 0.3, 
                             color = (0.19, 0.19, 0.33,1),
                             corners=(True,True,True,True))
        drawLabel(label = 'Play',
                  pos = (button_play_pos[0] + (buttons_size[0]/2), button_play_pos[1] + (buttons_size[1]/2)),
                  font_size = 22,
                  center = True)
        
        # Close
        drawRoundedRectangle(pos = button_close_pos,
                             radius = 8,
                             size = buttons_size,
                             precision = 0.3, 
                             color = (0.192, 0.192, 0.192, 1),
                             corners=(True,True,True,True))
        drawLabel(label = 'Close',
                  pos = (button_close_pos[0] + (buttons_size[0]/2), button_close_pos[1] + (buttons_size[1]/2)),
                  font_size = 22,
                  center = True)

    def on_touch_up(self, touch):
        x,y = list(touch.pos)
        a,b = list(self.btns_size)
        
        # click on play button
        if x > self.play_btn_pos[0] and x < self.play_btn_pos[0]+a and y > self.play_btn_pos[1] and y < self.play_btn_pos[1]+b:
            self.play()
            
        # click on close button
        elif x > self.close_btn_pos[0] and x < self.close_btn_pos[0]+a and y > self.close_btn_pos[1] and y < self.close_btn_pos[1]+b:
            self.close()
        
    def close(self):
        self.timer.cancel()
        if self.app_button:
            self.app_button.popup_closed()
        if self.get_root_window():
            self.get_root_window().remove_widget(self)
            
    def play(self):
        self.close()
        self.app.execute()

