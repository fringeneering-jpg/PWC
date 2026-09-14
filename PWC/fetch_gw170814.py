from gwpy.timeseries import TimeSeries

trigger_gps = 1186741861.0
start = trigger_gps - 16
end = trigger_gps + 16

print("Fetching H1...")
h1 = TimeSeries.fetch_open_data('H1', start, end, sample_rate=4096, cache=True)
h1.write('GW170814_H1_32s_4kHz.hdf5', overwrite=True)
print("H1 saved:", len(h1), "samples")

print("Fetching L1...")
l1 = TimeSeries.fetch_open_data('L1', start, end, sample_rate=4096, cache=True)
l1.write('GW170814_L1_32s_4kHz.hdf5', overwrite=True)
print("L1 saved:", len(l1), "samples")
