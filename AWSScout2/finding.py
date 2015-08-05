from AWSScout2.filter import *

# Import third-party packages
import dateutil.parser

#
# Base finding class
#
class Finding(Filter):

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.level = level
        self.questions = questions
        self.macro_items = []
        self.flagged_items = 0
        super(Finding, self).__init__(description, entity, callback, callback_args)

    def addItem(self, item, macro_item = None):
        if macro_item not in self.macro_items:
            self.flagged_items = self.flagged_items + 1
        super(Finding, self).addItem(item, macro_item)

    def removeItem(self, item, macro_item = None):
        super(Finding, self).removeItem(item, macro_item)
        if macro_item not in self.macro_items:
            self.flagged_items = self.flagged_items - 1

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

    # arg0: object attribute to check
    def isNotNull(self, key, obj):
        attribute = self.callback_args[0]
        if attribute in obj:
            if obj[attribute]:
                self.addItem(key)

    # arg0: object attribute to check (date)
    # arg1: date to compare with
    def wasCreatedBefore(self, key, obj):
        creation_date = dateutil.parser.parse(str(obj[self.callback_args[0]])).replace(tzinfo=None)
        expiration_date = dateutil.parser.parse(self.callback_args[1]).replace(tzinfo=None)
        age = (creation_date - expiration_date).days
        if (age < 0):
            return True
        else:
            return False

    # arg0: object attribute to check (instance type/class)
    # arg1:
    def checkUnscannableInstanceTypes(self, key, obj):
        if self.callback_args[0] in obj and len(self.callback_args) > 1:
            instance_type = obj[self.callback_args[0]]
            if instance_type in self.callback_args[1]:
                self.addItem(key)

    # arg0: object attribute to check (number)
    # arg1: threshold
    def isLessThan(self, key, obj):
        value = int(obj[self.callback_args[0]])
        threshold = int(self.callback_args[1])
        if value < threshold:
             self.addItem(key)

    # arg0: name of the attribute to check
    def isNotTrue(self, key, obj):
        value = bool(obj[self.callback_args[0]])
        if not value:
            self.addItem(key)
