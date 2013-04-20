RAW_DATA = []
N_COLS = 0
N_ROWS = 0
CELL_SIZE = 0
XLL_CENTER = 0
YLL_CENTER = 0

FILENAME = "latest.grid"

def IngestData(filename):
    global RAW_DATA, N_ROWS, N_COLS, CELL_SIZE, XLL_CENTER, YLL_CENTER
    if RAW_DATA:
        return
    f = open(filename, "r")
    l_parts = f.readline().strip().split()  # ncols C
    N_COLS = int(l_parts[1])
    l_parts = f.readline().strip().split()  # nrows R
    N_ROWS = int(l_parts[1])
    l_parts = f.readline().strip().split()  # xllcenter X
    XLL_CENTER = float(l_parts[1])
    l_parts = f.readline().strip().split()  # yllcenter Y
    YLL_CENTER = float(l_parts[1])
    l_parts = f.readline().strip().split()  # cell_size S
    CELL_SIZE = float(l_parts[1])
    f.readline()  # nodata_value, skip.
    for l in f:
        l = l.strip()
        try:
            RAW_DATA.append([float(x) for x in l.split()])
        except ValueError:
            # We've run out of data values.
            break


def GetSunExposure(lat, lng):
    if not RAW_DATA:
        IngestData(FILENAME)
    x_idx = int((float(lng) - XLL_CENTER) / CELL_SIZE)
    y_idx = N_ROWS - int((float(lat) - YLL_CENTER) / CELL_SIZE)
    return RAW_DATA[y_idx][x_idx]
