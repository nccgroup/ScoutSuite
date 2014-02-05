#!/usr/bin/env python

import json

# JSON-serializable dictionary
class FindingDictionary(dict):

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
