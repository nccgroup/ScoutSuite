#!/usr/bin/env python2

class Finding():

    def __init__(self, description, entity, callback, callback_args, level):
        self.description = description
        self.level = level
        self.entity = entity
        self.callback = callback
        self.callback_args = callback_args,
        self.level = level
        self.items = []
        self.macro_items = []

    def addItem(self, item, macro_item = None):
        self.items.append(item);
        if macro_item:
            self.macro_items.append(macro_item);

    def removeItem(self, item, macro_item = None):
        try:
            self.items.remove(item)
            if macro_item:
                self.macro_items.remove(macro_item)
        except:
            pass
