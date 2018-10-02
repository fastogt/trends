class TrendInfo(object):
    def __init__(self, key: str, trend_rate, trend_offset, mean, y_max, y_min, valid_dots_percent):
        self.key_ = key
        self.trend_rate_ = trend_rate
        self.trend_offset_ = trend_offset
        self.mean_ = mean
        self.y_max_ = y_max
        self.y_min_ = y_min
        self.valid_dots_percent_ = valid_dots_percent

    @property
    def key(self):
        return self.key_

    @property
    def trend_rate(self):
        return self.trend_rate_

    @property
    def trend_offset(self):
        return self.trend_offset_

    @property
    def trend(self):
        if self.trend_rate_ > 0:
            return 'rising'
        if self.trend_rate_ < 0:
            return 'falling'
        return 'constant'

    @property
    def mean(self):
        return self.mean_

    @property
    def y_min(self):
        return self.y_min_

    @property
    def y_max(self):
        return self.y_max_

    @property
    def valid_dots_percent(self):
        return self.valid_dots_percent_

    def to_dict(self) -> dict:
        return {
            'key': self.key,
            'trend_rate': self.trend_rate,
            'trend_offset': self.trend_offset,
            'trend': self.trend,
            'mean': self.mean,
            'max': self.y_max,
            'min': self.y_min,
            'valid_dots_percent': self.valid_dots_percent
        }

    def __lt__(self, other):
        return self.trend_rate < other.trend_rate

    def __str__(self):
        return str(self.to_dict())
