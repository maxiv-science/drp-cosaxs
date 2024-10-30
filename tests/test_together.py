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
            glob("data/*01dadc10f239.cbors"),
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
    assert list(f["pcap"].shape) == [3]
    assert round(f["pcap"][2][2], 6) == round(0.31000807, 6)
    assert f["pcap"].dtype.fields["I_t.Max"][0] == np.dtype("float64")

    stop_event.set()

    thread.join()
