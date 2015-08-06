from opinel.utils import printException
from AWSScout2.utils import ec2_classic

#
# Base filter
#
class Filter(object):

    def __init__(self, description, entity, callback, callback_args):
        self.description = description
        self.entity = entity
        self.callback = callback
        self.callback_args = callback_args
        self.items = []
        self.checked_items = 0

    def addItem(self, item, macro_item = None):
        if not macro_item:
            if item not in self.items:
                self.items.append(item)
        else:
            self.items.append(item)
            self.macro_items.append(macro_item)

    #
    # Call to that function when iterating over items or macro_items will create
    # invalid results.
    #
    def removeItem(self, item, macro_item = None):
        try:
            target = self.items.index(item)
            del self.items[target]
            if macro_item:
                del self.macro_items[target]
        except Exception as e:
            printException(e)
            pass

    def checkedNewItem(self):
        self.checked_items = self.checked_items + 1
