#!/usr/bin/env python2

class Finding():

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.description = description
        self.level = level
        self.entity = entity
        self.callback = callback
        self.callback_args = callback_args
        self.level = level
        self.questions = questions
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

    # arg0: limit
    # arg1: object attribute to count
    # arg2: condition attribute
    # arg3: condition value
    def hasMoreThan(self, key, obj):
        limit = self.callback_args[0]
        attribute = self.callback_args[1]
        condition_attr = self.callback_args[2]
        condition_val = self.callback_args[3]
        found_objects = [o for o in obj[attribute] if o[condition_attr] == condition_val]
        if len(found_objects) > int(limit):
            self.addItem(key)
