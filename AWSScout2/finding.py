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

    def addItem(self, item, macro_item):
        self.items.append(item);
        self.macro_items.append(macro_item);

    def removeItem(self, item, macro_item):
        self.items.remove(item)
        self.macro_items.remove(macro_item)
