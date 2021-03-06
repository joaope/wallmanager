from pymt import *
from mtmenu.ui.apppopup import AppPopup
from threading import Timer
from config import APPSLIST_BTN_SIZE, APPSLIST_BTN_IMAGE_SIZE, APPSLIST_BTN_FONT_SIZE, APPSLIST_BTN_POPUPS_PER_BTN, APPSLIST_STAR_ONLY_WHEN_ORDER_BY_RATING
from utils import get_trimmed_label_widget
from mtmenu import logger

class AppButton(MTKineticItem):
    """Widget representing an application on main window. 
    
    Arguments:
        app -- Application object attached to this widget
        kwargs -- Button properties, most of them inherited from MTButton
    
    This widget should be added to AppsGrid on Menu's UI construction"""
    def __init__(self, app, **kwargs):
        kwargs.setdefault('label', unicode(app))
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('size', APPSLIST_BTN_SIZE)        
        
        self.app = app
        self.popups_currently_open = 0
        self.double_tap_detected = False
        
        super(AppButton, self).__init__(**kwargs)
        
    """Execute application on double click
       Open popup on single click"""
    def on_press(self, touch):  
        self.double_tap_detected = touch.is_double_tap
        if touch.is_double_tap:
            self.double_tap_detected = False
            self.open_app()
        else:
            # Give it time before open popup because it can be a double-click
            Timer(0.5, self.open_popup, args=[touch.pos]).start()

    def open_popup(self, touch_pos):
        # If max number of popups allowed reached, don't open one more
        # If double click, don't open one more
        if self.popups_currently_open == APPSLIST_BTN_POPUPS_PER_BTN or self.double_tap_detected:
            return
        
        self.popups_currently_open += 1
        self.get_root_window().add_widget(AppPopup(self.app, touch_pos, self))

    def popup_closed(self):
        self.popups_currently_open -= 1

    def open_app(self):
        logger.info('\nLoading %s...\n' % unicode(self.app))
        logger.info('ID: %i' % self.app.id)
        logger.info('Path: %s\n' % self.app.get_extraction_fullpath())
        logger.info('Boot file: %s\n' % self.app.get_boot_file())
        self.app.execute()

        #refresh cstegory in main thread
        from mtmenu import categories_list
        categories_list.refresh()
        self.parent.refresh(categories_list.current)
        
        
    def draw(self): 
        # Outside line
        style = {'bg-color': (1, 1, 1, 1), 'draw-background': 0, 'draw-border': True, 'border-radius': 10}
        set_color(*style.get('bg-color'))
        drawCSSRectangle(pos=self.pos, size=self.size,  style = style)
        
        # Icon
        try:
            image = Image( "../webmanager/media/%s" % str(self.app.icon) )
            x,y = list(self.center)
            image.size = self.get_resized_size(image)
            image.pos = x - image.width /2, y - image.height /2      
            image.draw()
        except Exception, e:
            logger.error("EXCEPTION loading icon\n%s" % e)
        
        # Label
        label_obj, self.label = get_trimmed_label_widget(text = self.label,
                                                         position = (self.pos[0] / 2, self.size[1]-50),
                                                         font_size = APPSLIST_BTN_FONT_SIZE,
                                                         max_width = self.size[0] - 5)
        label_obj.pos = (self.pos[0] + ((self.size[0] - label_obj.width) / 2),
                         self.pos[1] - APPSLIST_BTN_FONT_SIZE - 6)
        label_obj.draw()
        
        # Show star only if is configured to always appears or if order by 'Rating' is selected
        from mtmenu import apps_list
        
        if not APPSLIST_STAR_ONLY_WHEN_ORDER_BY_RATING or (APPSLIST_STAR_ONLY_WHEN_ORDER_BY_RATING and apps_list.criteria == 'value'):
        # Star
            star_size = (48,48)
            star_pos_x = self.pos[0] + self.size[0] - star_size[0]/3*2
            star_pos_y = self.pos[1] + self.size[1] - star_size[1]/3*2
            
            image = Image("images/star.png")
            image.pos = (star_pos_x, star_pos_y)
            image.draw()
            
            # Star number
            drawLabel(label = int(self.app.stars()),
                      pos = (star_pos_x + star_size[0]/2, star_pos_y + star_size[1]/2),
                      font_size = 25,
                      center = True)
    
    @staticmethod
    def get_resized_size (image):
        
        width, height = image.width, image.height
        max_width, max_height = list(APPSLIST_BTN_IMAGE_SIZE)
        
        # If width and height not higher than allowed, all good
        if width <= max_width and height <= max_height:
            return (width, height)
        
        # Scale maintaining aspect ratio
        scale = min(float(max_width) / width, 
                    float(max_height) / height)

        return (width * scale, height * scale)


