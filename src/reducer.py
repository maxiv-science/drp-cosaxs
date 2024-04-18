import logging
from pathlib import Path

from dranspose.event import ResultData
from dranspose.parameters import StrParameter, BoolParameter
import os
import h5py
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

class CosaxsReducer:
    def __init__(self, parameters=None,  context=None,**kwargs):
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
            #write data to h5 file
            #push data to hsds
            pass

    def finish(self, parameters=None):

        if self._fh:
            self._fh.close()
