from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Components.config import config
from Components.Converter.Poll import Poll

class lsPicsmap(Renderer, Poll):
    __module__ = __name__

    def __init__(self):
        Poll.__init__(self)
        Renderer.__init__(self)
        self.nameCache = {}
        self.pngname = ''
        self.pixmaps = []
        self.pixdelay = 300
        self.control = 0
        self.pics = []
        self.picon_default = 'picon_default.png'

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'pixmaps':
                self.pixmaps = value.split(',')
            elif attrib == 'pixdelay':
                self.pixdelay = int(value)
            elif attrib == 'control':
                self.control = int(value)
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        self.poll_interval = 2000
        self.poll_enabled = True
        if self.instance:
            pngname = ''
            if what[0] != self.CHANGED_CLEAR:
                self.runAnim()

    def runAnim(self):
        if len(self.pics) == 0:
            for x in self.pixmaps:
                self.pics.append(LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, x)))

        self.slide = len(self.pics)
        self.timer = eTimer()
        self.timer.callback.append(self.timerEvent)
        self.timer.start(self.pixdelay, True)

    def timerEvent(self):
        if self.control > 0:
            if self.slide == 0:
                self.slide = len(self.pics)
            self.timer.stop()
            self.instance.setPixmap(self.pics[len(self.pics) - self.slide])
            self.slide = self.slide - 1
            self.timer.start(self.pixdelay, True)
        elif self.control == 0:
            if self.slide > 0:
                self.timer.stop()
                self.instance.setPixmap(self.pics[len(self.pics) - self.slide])
                self.slide = self.slide - 1
                self.timer.start(self.pixdelay, True)
            else:
                self.timer.stop()
        else:
            self.timer.stop()