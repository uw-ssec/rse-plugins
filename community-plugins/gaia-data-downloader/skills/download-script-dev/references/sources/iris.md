# IRIS Seismic

**Description:** Seismic waveform and station data from the International Federation of Digital Seismograph Networks (FDSN).

**Access Pattern:** FDSN web services via `obspy`

**Authentication:** None

**Key Libraries:** `obspy`

**Access Example:**
```python
from obspy.clients.fdsn import Client
from obspy import UTCDateTime

client = Client("IRIS")
st = client.get_waveforms(
    network="UW", station="RCM", location="--", channel="HHZ",
    starttime=UTCDateTime("2024-01-15"), endtime=UTCDateTime("2024-01-16"),
)
```

**Notes:**
- Seismic data, not hydroclimatological — included for cross-domain GAIA studies
- `obspy` handles all FDSN protocol details
- Station inventory available via `client.get_stations()`
