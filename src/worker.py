import logging
import tempfile
import json

from dranspose.event import EventData
from dranspose.parameters import IntParameter, StrParameter, BoolParameter
from dranspose.middlewares.stream1 import parse
from dranspose.middlewares.sardana import parse as sardana_parse
from dranspose.data.stream1 import Stream1Data, Stream1Start
import numpy as np
from numpy import unravel_index

logger = logging.getLogger(__name__)


class CosaxsWorker:

    @staticmethod
    def describe_parameters():
        params = [
            IntParameter(name="qx", default=100),
            IntParameter(name="qy", default=100),
        ]
        return params

    def __init__(self, parameters, context, **kwargs):
        if "ai" not in context:
            context["ai"] = 5

    def process_event(self, event: EventData, parameters=None):
        ret = {}

        dat = None
        if "pilatus" in event.streams:
            dat = parse(event.streams["pilatus"])
        print("image data", dat)
        if dat:
            if isinstance(dat, Stream1Start):
                print("start message", dat)
                return {**ret, "processed_filename": dat.filename}
            if not isinstance(dat, Stream1Data):
                return None

            # your code here
            # return whatever you need in reduce
            return {"img": dat.data , "cropped": None}


    def finish(self, parameters=None):
        print("finished")
