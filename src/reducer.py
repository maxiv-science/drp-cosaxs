import logging
from pathlib import Path

from dranspose.event import ResultData
from dranspose.parameters import StrParameter, BoolParameter
import os
import h5py
import h5pyd
import numpy as np
from datetime import datetime
import time
from copy import copy

logger = logging.getLogger(__name__)


class CosaxsReducer:
    def __init__(self, parameters=None, context=None, **kwargs):
        self._fh = None
        self.publish = {}
        self.processed_filename = None

    def process_result(self, result: ResultData, parameters=None):
        if result.payload is None:
            return

        if "processed_filename" in result.payload:
            self.pileup_filename = result.payload["processed_filename"]
            # open file and put into self._fh
        if "img" in result.payload:
            # write data to h5 file
            # push data to hsds
            pass

        if "pcap_start" in result.payload:
            # for field in result.payload["pcap_start"]:
            # self.hsds["pcap"].require_dataset(field.name, shape=(10000,), dtype=field.type)
            #    pass
            rawcol_names = [field.name for field in result.payload["pcap_start"]]
            connmap = {"FMC_IN.VAL3": "I_t", "FMC_IN.VAL6": "I_0"}
            col_names = []
            for cn in rawcol_names:
                chg = cn
                for fr, to in connmap.items():
                    chg = chg.replace(fr, to)
                col_names.append(chg)
            print("col names", col_names)
            self.ds_dt = np.dtype(
                {"names": col_names, "formats": [(float)] * len(col_names)}
            )
            self.publish["pcap"] = np.array([], dtype=self.ds_dt)

        if "pcap" in result.payload:
            data = {}
            for field in result.payload["pcap"].fields.values():
                data[field.name] = field.value
                # oldsize = self.hsds["pcap"][field.name].shape
                # print(oldsize)
                # self.hsds["pcap"][field.name].resize(oldsize[0] + 1, axis=0)
                # self.hsds["pcap"][field.name][result.event_number] = field.value

                # self.cg_ds = self.hsds["basler"].require_dataset("cg", shape=(2,), dtype=float)
            # should put value at correct event number
            delta = np.array(tuple(data.values()), dtype=self.ds_dt)
            self.publish["pcap"] = np.append(self.publish["pcap"], delta)
            # time.sleep(1)
            # print("data", result.event_number, data)
            # self.hsds["pcap/data"][5*result.event_number:5*result.event_number+5] = []*5
            # self.hsds["frame"][()] = int(result.event_number)

    def finish(self, parameters=None):
        if self._fh:
            self._fh.close()
