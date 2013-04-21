class SolarExposure(object):
    
    def __init__(self, filename, duration):
        self.raw_data = []
        self.n_cols = 0
        self.n_rows = 0
        self.cell_size = 0.0
        self.xll_center = 0.0
        self.yll_center = 0.0
        self.last_updated = None
        self.filename = filename
        self.duration = duration

    def IngestData(self):
        if self.raw_data:
            return
        f = open(self.filename, "r")
        l_parts = f.readline().strip().split()  # ncols C
        self.n_cols = int(l_parts[1])
        l_parts = f.readline().strip().split()  # nrows R
        self.n_rows = int(l_parts[1])
        l_parts = f.readline().strip().split()  # xllcenter X
        self.xll_center = float(l_parts[1])
        l_parts = f.readline().strip().split()  # yllcenter Y
        self.yll_center = float(l_parts[1])
        l_parts = f.readline().strip().split()  # cell_size S
        self.cell_size = float(l_parts[1])
        f.readline()  # nodata_value, skip.
        for l in f:
            l = l.strip()
            try:
                self.raw_data.append([float(x) for x in l.split()])
            except ValueError:
                # We've run out of data values.
                break
        for footer in f:
            if footer.startswith("LAST UPDATED"):
                self.last_updated = footer.split()[2]
                break

    def GetLastUpdated():
        if not self.last_updated:
            self.IngestData()
        return self.last_updated

    def GetSunExposure(self, lat, lng):
        if not self.raw_data:
            self.IngestData()
        x_idx = int((float(lng) - self.xll_center) / self.cell_size)
        y_idx = self.n_rows - int(
            (float(lat) - self.yll_center) / self.cell_size)
        return self.raw_data[y_idx][x_idx]


class DailySolarExposure(SolarExposure):
    
    def __init__(self, filename):
        super(DailySolarExposure, self).__init__(filename, duration="daily")


class MonthlyAverageSolarExposure(SolarExposure):
    
    def __init__(self, filename):
        super(MonthlyAverageSolarExposure, self).__init__(
            filename, duration="month")
        
    def GetSunExposure(self, lat, lng):
        return 30 * super(MonthlyAverageSolarExposure, self).GetSunExposure(
            lat, lng)
