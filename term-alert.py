#!/bin/python3
import os
import urwid
import time

bad_files_to_search = ['testfile']

def signal_alert():
    signal = False
    message = 'ALERT!'
    for file in bad_files_to_search:
        if (os.path.exists(file)):
            signal = True
            message += '\n' + file + ' exists'
    if signal:
        return (True, message) 
    return (False, 'nothing')

class Alert:
    def __init__(self):
        self.loop = None
        self.animate_alarm = None
        self.placeholder = urwid.SolidFill()
        self.palette = []

    def update_screen(self):
        result = signal_alert()
        if result[0]:
            self.alert_screen(result[1])
        else:
            self.calm_screen()
        self.loop.screen.clear()
            
    def handle_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        else:
            self.update()

    def alert_screen(self, message):
        self.palette = [
            ('banner', '', '', '', '#ffa', '#60d'),
            ('streak', '', '', '', 'g50', '#60a'),
            ('inside', '', '', '', 'g38', '#808'),
            ('outside', '', '', '', 'g27', '#a06'),
            ('bg', '', '', '', 'g7', '#d06'),]
        self.txt.set_text(('banner', message))
        if self.loop:
            self.loop.screen.register_palette(self.palette)
            self.loop.widget = urwid.AttrMap(self.placeholder, 'bg')
            self.loop.widget.original_widget = urwid.Filler(urwid.Pile([]))
            div = urwid.Divider()
            outside = urwid.AttrMap(div, 'outside')
            inside = urwid.AttrMap(div, 'inside')
            streak = urwid.AttrMap(self.txt, 'streak')
            pile = self.loop.widget.base_widget # .base_widget skips the decorations
            for item in [outside, inside, streak, inside, outside]:
                pile.contents.append((item, pile.options()))

    def calm_screen(self):
        self.palette = [
            ('banner', '', '', '', '#ffa', '#066'),
            ('streak', '', '', '', '#066', '#066'),
            ('inside', '', '', '', '#076', '#076'),
            ('outside', '', '', '', '#0a5', '#0a5'),
            ('bg', '', '', '', '#0c5', '#0c5'),]
        self.txt.set_text(('banner', u'nothing'))
        if self.loop:
            self.loop.screen.register_palette(self.palette)
            self.loop.widget = urwid.AttrMap(self.placeholder, 'bg')
            self.loop.widget.original_widget = urwid.Filler(urwid.Pile([]))
            div = urwid.Divider()
            outside = urwid.AttrMap(div, 'outside')
            inside = urwid.AttrMap(div, 'inside')
            streak = urwid.AttrMap(self.txt, 'streak')
            pile = self.loop.widget.base_widget # .base_widget skips the decorations
            for item in [outside, inside, streak, inside, outside]:
                pile.contents.append((item, pile.options()))

    def draw(self):
        self.txt = urwid.Text(('banner', u'loading...'), align='center')
        self.loop = urwid.MainLoop(self.placeholder, self.palette, unhandled_input=self.handle_input)
        
        self.loop.screen.set_terminal_properties(colors=256)
        self.loop.widget = urwid.AttrMap(self.placeholder, 'bg')
        self.loop.widget.original_widget = urwid.Filler(urwid.Pile([]))
        div = urwid.Divider()
        outside = urwid.AttrMap(div, 'outside')
        inside = urwid.AttrMap(div, 'inside')
        streak = urwid.AttrMap(self.txt, 'streak')
        pile = self.loop.widget.base_widget # .base_widget skips the decorations
        pile.contents.clear()
        for item in [outside, inside, streak, inside, outside]:
            pile.contents.append((item, pile.options()))
        self.loop.run()

    def update(self, loop=None, user_data=None):
        self.update_screen()
        self.animate_alarm = self.loop.set_alarm_in(0.1, self.update)

def main():
    Alert().draw()

if '__main__'==__name__:
    main()
