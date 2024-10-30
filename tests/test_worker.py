import logging
import threading
from glob import glob

import h5pyd
import numpy as np
from dranspose.replay import replay


def test_livequery():
    stop_event = threading.Event()
    done_event = threading.Event()

    thread = threading.Thread(
        target=replay,
        args=(
            "src.worker:CosaxsWorker",
            "src.reducer:CosaxsReducer",
            ["data/pcaptestpcap-ingester-7961ecb0-4844-4b47-a0a2-e0855c37dd79.pkls"],
            None,
            "testparams.json",
        ),
        kwargs={"port": 5010, "stop_event": stop_event, "done_event": done_event},
    )
    thread.start()

    # do live queries

    done_event.wait()

    f = h5pyd.File("http://localhost:5010/", "r")
    logging.info("file %s", list(f.keys()))
    logging.info("pcap %s", f["pcap"])
    logging.info("pcap data %s", f["pcap"][:])
    logging.info("pcap type %s", f["pcap"].dtype)
    assert list(f["pcap"].shape) == [6]
    assert round(f["pcap"][5][2], 6) == round(1.53887866, 6)
    assert f["pcap"].dtype.fields["I_t.Max"] == (np.dtype("float64"), 8)

    stop_event.set()

    thread.join()
