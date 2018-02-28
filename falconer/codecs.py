from enum import Enum

import simplejson as json


class ImprovedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o.name

        return super(ImprovedJSONEncoder, self).default(o)
