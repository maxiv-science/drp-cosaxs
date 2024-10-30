import logging
import tempfile
import json

from dranspose.event import EventData
from dranspose.parameters import IntParameter, StrParameter, BoolParameter
from dranspose.middlewares.stream1 import parse
from dranspose.middlewares.sardana import parse as sardana_parse
from dranspose.middlewares.positioncap import PositioncapParser
from dranspose.data.positioncap import PositionCapValues, PositionCapStart
from datetime import timedelta
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
        self.pcap = PositioncapParser()

    def process_event(self, event: EventData, parameters=None, **kwargs):
        ret = {}

        dat = None
        if "pilatus" in event.streams:
            dat = parse(event.streams["pilatus"])
        print("image data", dat)
        if dat:
            if isinstance(dat, Stream1Start):
                # return {**ret, "processed_filename": dat.filename}
                ret["processed_filename"] = dat.filename
            if not isinstance(dat, Stream1Data):
                pass

            # your code here
            # return whatever you need in reduce
            # return {"img": dat.data, "cropped": None}

        if "pcap" in event.streams:
            res = self.pcap.parse(event.streams["pcap"])
            if isinstance(res, PositionCapStart):
                ret["pcap_start"] = self.pcap.fields

            if isinstance(res, PositionCapValues):
                triggertime = timedelta(seconds=res.fields["PCAP.TS_TRIG.Value"].value)
                logger.debug(
                    "got values %s at timestamp %s",
                    res,
                    self.pcap.arm_time + triggertime,
                )
                ret.update({"pcap": res, "time": self.pcap.arm_time + triggertime})
        if len(ret) > 0:
            return ret

    def finish(self, parameters=None):
        print("finished")
