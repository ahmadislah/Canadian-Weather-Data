"""
Assignment 0
CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.
"""

from datetime import date, timedelta
from typing import Tuple, Dict, Optional, TextIO, Union
import os

# The column numbers where each kind of information appears.  For example,
# column 9 contains maximum temperature.
LONG, LAT = 0, 1
STN_NAME, CL_ID = 2, 3
DATE, YEAR, MONTH, DAY = 4, 5, 6, 7
DATA_QUALITY = 8
MAX_TEMP, MAX_TEMP_FLAG = 9, 10
MIN_TEMP, MIN_TEMP_FLAG = 11, 12
MEAN_TEMP, MEAN_TEMP_FLAG = 13, 14
HEAT_DEG_DAYS, HEAT_DEG_DAYS_FLAG = 15, 16
COOL_DEG_DAYS, COOL_DEG_DAYS_FLAG = 17, 18
TOTAL_RAIN, TOTAL_RAIN_FLAG = 19, 20
TOTAL_SNOW, TOTAL_SNOW_FLAG = 21, 22
TOTAL_PRECIP, TOTAL_PRECIP_FLAG = 23, 24
SNOW_ON_GRND, SNOW_ON_GRND_FLAG = 25, 26
DIR_MAX_GUST, DIR_MAX_GUST_FLAG = 27, 28
SPD_MAX_GUST, SPD_MAX_GUST_FLAG = 29, 30


class DailyWeather:
    """Weather facts for a single day.

    === Instance Attributes ===
    avg_temp: Average temperature on this day, in degrees Celsius
    low_temp: Minimum temperature on this day, in Celsius
    high_temp: Maximum temperature on this day, in Celsius
    precipitation: Total precipitation on this day in mm,
        or -1 if there were only "trace amounts" of precipitation
    rainfall: Total rainfall on this day in mm,
        or -1 for trace amounts
    snowfall: Total snowfall on this day in cm,
        or -1 for trace amounts

    === Representation Invariants ===
    - precipitation >= -1
    - rainfall >= -1
    - snowfall >= -1
    - low_temp <= avg_temp <= high_temp

    === Sample Usage ===
    >>> weather = DailyWeather((13.1, 9.2, 20.3), (5, 0, 0))
    >>> print(weather.avg_temp)
    13.1
    >>> print(weather.low_temp)
    9.2
    >>> print(weather.high_temp)
    20.3
    >>> print(weather.precipitation)
    5
    """
    avg_temp: float
    low_temp: float
    high_temp: float
    precipitation: float
    snowfall: float
    rainfall: float

    def __init__(self, temperature_statistics: Tuple[float, float, float],
                 precipitation_statistics: Tuple[float, float, float]) -> None:
        """Initialize this day's weather.

        temperature_statistics[0] is the average temperature in Celsius
        temperature_statistics[1] is the minimum temperature in Celsius
        temperature_statistics[2] is the maximum temperature in Celsius

        precipitation_statistics[0] is the total precipitation in mm
        precipitation_statistics[1] is the total rainfall in mm
        precipitation_statistics[2] is the total snowfall in cm

        For all values, -1 indicates trace amounts.

        Preconditions:
            - all float values in the tuples are >= -1
            - minimum temperature <= average temperature <= high temperature

        >>> weather = DailyWeather((13.1, 9.2, 20.3), (5, 0, 0))
        >>> print(weather.avg_temp)
        13.1
        """
        self.avg_temp = temperature_statistics[0]
        self.low_temp = temperature_statistics[1]
        self.high_temp = temperature_statistics[2]
        self.precipitation = precipitation_statistics[0]
        self.rainfall = precipitation_statistics[1]
        self.snowfall = precipitation_statistics[2]

    # Note: We will just test that the string returned includes the 6 values,
    # We will not test the full content or format of the string.
    def __str__(self) -> str:
        """Return a str representing this DailyWeather.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> print(weather)
        Average: 13 Low: 9 High: 20 Precipitation: 5 Snow: 0 Rain: 0
        """
        return "Average: " + str(self.avg_temp) + " Low: " + str(self.low_temp)\
               + " High: " + str(self.high_temp) + " Precipitation: " + \
               str(self.precipitation) + " Snow: " + str(self.snowfall) + \
               " Rain: " + str(self.rainfall)


class HistoricalWeather:
    """A record of historical weather information for a fixed place on Earth.

    === Instance Attributes ===
    name: The name of the place for which the weather is being recorded.
    coordinates: The latitude and longitude of this place.

    === Private Attributes ===
    _records: The daily weather records for this place. Each key is a
        date and its value is the location's weather on that day. There may
        be gaps in the data. For example, there could be data for Jan 1, 2020
        and Jan 5, 2020, but not for the days in between.

    === Representation Invariants ===
    - coordinates[0] is a valid latitude (between -90 and 90)
    - coordinates[1] is a valid longitude (between -180 and 180)

    === Sample Usage ===
    >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
    >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    >>> toronto_weather.add_weather(date.today(), weather)
    >>> print(toronto_weather.name)
    Toronto
    >>> print(toronto_weather.coordinates)
    (43.6529, -79.3849)
    >>> print(toronto_weather.retrieve_weather(date.today()).avg_temp)
    13
    """
    name: str
    coordinates: Tuple[float, float]
    _records: Dict[date, DailyWeather]

    def __init__(self, name: str, coordinates: Tuple[float, float]) -> None:
        """Initialize this historical weather record with these coordinates,
        place name, and no recorded weather so far.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> print(toronto_weather.name)
        Toronto
        """
        self.name = name
        self.coordinates = coordinates
        self._records = {}

    # We will not test this method, but we recommend that you write and use it.
    def __str__(self) -> str:
        """Return a str representing this HistoricalWeather.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> loc = HistoricalWeather('Toronto', (43.6, -79.63))
        >>> loc.add_weather(date(2020,7,13), weather)
        >>> print(loc)
        Toronto (43.6, -79.63):
        2020-07-13: Average: 13 Low: 9 High: 20 Precipitation: 5 Snow: 0 \
Rain: 0
        """
        data = self.name + " " + str(self.coordinates) + ":" + "\n"
        count = 0
        dates = list(self._records.keys())
        n = len(dates)  # number of keys
        for d in dates:
            if d.month >= 10:
                data = data + str(d.year) + "-" + str(d.month) + "-" \
                    + str(d.day) + ": " + str(self._records[d])
            else:  # adding leading zero to the month
                data = data + str(d.year) + "-0" + str(d.month) + "-" \
                    + str(d.day) + ": " + str(self._records[d])
            if count + 1 < n:
                data = data + "\n"
                count += 1
        return data

    def add_weather(self, d: date, w: DailyWeather) -> None:
        """Record that w was the weather on the date d.

        If a record for date d already exists, then do nothing (i.e. do not
        change the information that is already recorded).

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> print(toronto_weather.retrieve_weather(date.today()).avg_temp)
        13
        """
        if d not in list(self._records.keys()):
            self._records[d] = w

    def retrieve_weather(self, d: date) -> Optional[DailyWeather]:
        """Return the weather on day d if available, otherwise return None.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> toronto_weather.retrieve_weather(date.today()).avg_temp == 13
        True
        """
        if d in list(self._records.keys()):
            return self._records[d]
        else:
            return None

    def record_high(self, m: int, d: int) -> float:
        """Return the highest temperature recorded at this location on month m
        and day d in any year. Note that months are represented by numbers 1-12.

        Preconditions:
            - 1 <= m <= 12
            - 1 <= d <= 31 and d is possible day for the month m. For example,
              if m is 9 (for September), m will not be 31, since September has
              30 days.
            - The weather on month m and day d has been recorded for this
              location in at least one year.

        >>> weather1 = DailyWeather((13, 10, 40), (0, 0, 0))
        >>> weather2 = DailyWeather((13, 10, 30), (0, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> day1 = date(2020, 6, 8)
        >>> day2 = date(2019, 6, 8)
        >>> toronto_weather.add_weather(day1, weather1)
        >>> toronto_weather.add_weather(day2, weather2)
        >>> toronto_weather.record_high(6, 8)
        40
        """
        highest_temp = -100000.0
        dates = list(self._records.keys())
        for days in dates:
            if days.month == m and days.day == d and \
                    self._records[days].high_temp > highest_temp:
                highest_temp = self._records[days].high_temp
        return highest_temp

    def monthly_average(self) -> Dict[str, float]:
        """For each of the 12 months, return the average of the minimum
        temperatures for all dates in that month (in any year) that have
        weather recorded.

        Return the result in a dictionary mapping month name to average,
        and using these three-character names for the months:
            Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec.
        If a month has no weather recorded in any year, map that month name
        to the value None.

        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> jan1_weather = DailyWeather((13, 11, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2019, 1, 1), jan1_weather)
        >>> jan2_weather = DailyWeather((13, 10, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2019, 1, 2), jan2_weather)
        >>> jan2020_weather = DailyWeather((13, 0, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2020, 1, 18), jan2020_weather)
        >>> feb_weather = DailyWeather((13, 11, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2019, 2, 1), feb_weather)
        >>> d = toronto_weather.monthly_average()
        >>> d['Jan'] == 7.0
        True
        >>> d['Feb'] == 11.0
        True
        >>> d['Mar'] is None
        True
        """
        months = {'Jan': None, 'Feb': None, 'Mar': None, 'Apr': None,
                  'May': None, 'Jun': None, 'Jul': None, 'Aug': None,
                  'Sep': None, 'Oct': None, 'Nov': None, 'Dec': None}
        num_to_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
                        6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                        11: 'Nov', 12: 'Dec'}
        avg_temp = 0
        sums = 0
        num_days = 0  # number of recorded temperatures that month
        count = 1  # starting with January
        dates = list(self._records.keys())
        while count <= 12:
            for days in dates:
                if days.month == count:
                    sums += self._records[days].low_temp
                    num_days += 1
            if num_days > 0:
                avg_temp = sums / num_days
                months[num_to_month[count]] = avg_temp
            avg_temp = 0
            sums = 0
            num_days = 0
            count += 1
        return months

    def contiguous_precipitation(self) -> Tuple[date, int]:
        """Return the start date and length of the longest sequence of
        consecutive days that had precipitation.

        A day is considered to have had precipitation if its precipitation
        value is either above 0 or is -1 (indicating that there were trace
        amounts of precipitation). The days in a sequence must have been
        consecutive, that is, there can be no day between them. For example.
        if we have recorded weather for July 3rd, 5th, and 6th, that is not
        a sequence of consecutive days.

        In the case of a tie for the longest sequence, any one of the tied
        start dates can be returned.

        Precondition: At least one day's weather has been recorded.

        >>> weather1 = DailyWeather((0, 0, 0), (1, 0, 0))
        >>> weather2 = DailyWeather((0, 0, 0), (2, 0, 0))
        >>> weather3 = DailyWeather((0, 0, 0), (0, 0, 0))
        >>> weather4 = DailyWeather((0, 0, 0), (1, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> day = timedelta(days=1)
        >>> toronto_weather.add_weather(date.today(), weather1)
        >>> toronto_weather.add_weather(date.today() + day, weather2)
        >>> toronto_weather.add_weather(date.today() + 2 * day, weather3)
        >>> toronto_weather.add_weather(date.today() + 3 * day, weather4)
        >>> result = toronto_weather.contiguous_precipitation()
        >>> result[0] == date.today()
        True
        >>> result[1]
        2
        """
        dates = sorted(list(self._records.keys()))  # dates sorted
        n = len(dates)
        day = timedelta(days=1)
        count = 0  # consecutive days of precipitation
        max_count = 0
        first_day = 0  # first day of precipitation
        max_first_day = dates[0]
        consecutive = False
        for j in range(n):
            if consecutive and dates[j] == dates[j - 1] + day \
                    and (self._records[dates[j]].precipitation == -1
                         or self._records[dates[j]].precipitation > 0):
                count += 1
                consecutive = True
                if count > max_count:
                    max_count = count
                    max_first_day = first_day
            elif self._records[dates[j]].precipitation == -1 or \
                    self._records[dates[j]].precipitation > 0:
                count = 1
                consecutive = True
                first_day = dates[j]
                if count > max_count:
                    max_count = count
                    max_first_day = first_day
            else:
                count = 0
                consecutive = False
        return max_first_day, max_count

    def percentage_snowfall(self) -> float:
        """Return the fraction of the snowfall and rainfall at this location
        that was snowfall, across all dates when weather was recorded there.

        The answer returned should be calculated as:
            total snowfall / (total snowfall + total rainfall)

        Do not count trace amounts in this calculation. Ignore the units in
        the calculation.  (This is equivalent to assuming that 1 mm of
        rain is equivalent to 1 cm of snow.)

        Precondition: At least one day's weather has been recorded where
            snowfall > 0 or rainfall > 0 or both.

        >>> weather1 = DailyWeather((0, 0, 0), (1, 0, 1))
        >>> weather2 = DailyWeather((0, 0, 0), (3, 3, 0))
        >>> today = date(2020, 5, 1)
        >>> day = timedelta(days=1)
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(today, weather1)
        >>> toronto_weather.add_weather(today + day, weather2)
        >>> toronto_weather.percentage_snowfall()
        0.25
        """
        total_snow = 0
        total_rain = 0
        dates = list(self._records.keys())
        for days in dates:
            if self._records[days].snowfall > 0:
                total_snow += self._records[days].snowfall
            if self._records[days].rainfall > 0:
                total_rain += self._records[days].rainfall
        return total_snow / (total_snow + total_rain)


class Country:
    """ The weather records for various locations in a country.

    === Instance Attributes ===
    name: Name of the country.

    === Private Attributes ===
    _histories:
        The weather records for this country. Each key is a locations's name
        and it's value is that locations's weather history

    === Sample Usage ===
    >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
    >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
    >>> toronto_weather.add_weather(date.today(), weather)
    >>> canada = Country('Canada')
    >>> canada.add_history(toronto_weather)
    >>> yyz = canada.retrieve_history('YYZ')
    >>> yyz.retrieve_weather(date.today()).avg_temp == 13
    True

    === Representation Invariants ===
    - For each key, k, of _histories, k == _histories[k].name
    """

    name: str
    _histories: Dict[str, HistoricalWeather]

    def __init__(self, n: str) -> None:
        """ Initialize this Country with name n and no weather history so far.

        >>> canada = Country('Canada')
        >>> print(canada.name)
        Canada
        """
        self.name = n
        self._histories = {}

    # We will not test this method, but recommend that you write and use it.
    def __str__(self) -> str:
        """Return a str representing this Country.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> weather_2 = DailyWeather((14, 10, 21), (5, 0, 2.0))
        >>> canada = Country('Canada')
        >>> the_date = date(2020,7,13)
        >>> loc1_data = HistoricalWeather('Toronto', (43.6, -79.63))
        >>> loc1_data.add_weather(the_date, weather)
        >>> loc2_data = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> loc2_data.add_weather(the_date - timedelta(1), weather)
        >>> loc2_data.add_weather(the_date + timedelta(1), weather_2)
        >>> canada.add_history(loc1_data)
        >>> canada.add_history(loc2_data)
        >>> print(canada)
        Canada:
        Toronto (43.6, -79.63):
        2020-07-13: Average: 13 Low: 9 High: 20 Precipitation: 5 Snow: 0 \
Rain: 0
        YYZ (43.6529, -79.3849):
        2020-07-12: Average: 13 Low: 9 High: 20 Precipitation: 5 Snow: 0 \
Rain: 0
        2020-07-14: Average: 14 Low: 10 High: 21 Precipitation: 5 Snow: 2.0 \
Rain: 0
        """
        data = self.name + ":\n"
        history = list(self._histories.keys())
        n = len(history)
        count = 0
        for place in history:
            data = data + str(self._histories[place])
            if count + 1 < n:
                data = data + "\n"
            count += 1
        return data

    def add_history(self, hw: HistoricalWeather) -> None:
        """ Add a location to this Country. hw is the location's weather
        history, and hw.name is the location's name.

        If a location with the name hw.name is already recorded in this Country,
        then do nothing (i.e. do not change the data that is already present
        for that location).

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> canada = Country('Canada')
        >>> canada.add_history(toronto_weather)
        >>> yyz = canada.retrieve_history('YYZ')
        >>> yyz.retrieve_weather(date.today()).avg_temp == 13
        True
        """
        if hw.name not in list(self._histories.keys()):
            self._histories[hw.name] = hw

    def retrieve_history(self, name: str) -> Optional[HistoricalWeather]:
        """Return the weather history for the location called name, or
        None if no such location has been recorded in this Country.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> canada = Country('Canada')
        >>> canada.add_history(toronto_weather)
        >>> yyz = canada.retrieve_history('YYZ')
        >>> yyz.retrieve_weather(date.today()).avg_temp == 13
        True
        """
        if name in list(self._histories.keys()):
            return self._histories[name]
        else:
            return None

    def snowiest_location(self) -> Union[Tuple[str, float], Tuple[None, None]]:
        """Return the name of location with the highest percentage snowfall in
        this Country, and its percentage snowfall.

        In the case of a tie, any one of the tied locations can be returned.

        If there are no locations in this Country, return (None, None).

        Precondition: For all locations in this Country, at least one day's
            weather has been recorded where snowfall > 0 or rainfall > 0
            or both.

        >>> weather = DailyWeather((13, 9, 20), (5, 2, 3))
        >>> other_weather = DailyWeather((13, 4, 20), (5, 2, 2))
        >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> mtl_weather = HistoricalWeather('Montreal', (45.47, -73.74))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> mtl_weather.add_weather(date.today(), other_weather)
        >>> canada = Country('Canada')
        >>> canada.add_history(toronto_weather)
        >>> canada.add_history(mtl_weather)
        >>> result = canada.snowiest_location()
        >>> result[0]
        'YYZ'
        >>> result[1]
        0.6
        """
        if self._histories == {}:
            return None, None
        history = list(self._histories.keys())
        max_snowfall = 0
        max_place = history[0]
        for place in history:
            snowfall = self._histories[place].percentage_snowfall()
            if snowfall > max_snowfall:
                max_snowfall = snowfall
                max_place = place
        return max_place, max_snowfall

    def generate_summary(self) -> None:
        """
        Write a summary of interesting statistics for the locations
        in this Country to a markdown file called report.md

        Precondition:
        - All locations in this Country have at least one row of data
          recorded in December of any year
        - Data has been recorded for Dec 25 in at least one year
        """

        headers = ["Location", "record high <br/> for Dec 25",
                   "december <br/> average",
                   "contiguous <br/> precipitation",
                   "percentage <br/> snowfall"]

        with open("report.md", 'w') as f:
            f.write(" | ".join(headers) + "\n")
            f.write(":|-".join(["-" * len(col) for col in headers]) + ":\n")
            for key in self._histories:
                loc = self._histories[key]
                (rec_high, mon_avg,
                 ctgs_prec, perc_snow) = (loc.record_high(12, 25),
                                          loc.monthly_average(),
                                          loc.contiguous_precipitation(),
                                          loc.percentage_snowfall())
                f.write(f"{key : <20} | {rec_high : <10.4} | "
                        f"{mon_avg['Dec']} | "
                        f"{ctgs_prec[1] : <24} | {perc_snow : <18.2}\n")


def load_data(f: TextIO) -> Optional[HistoricalWeather]:
    """Return a HistoricalWeather record representing the weather data in the
    already open csv file f.

    If f contains no lines of data aside from its header, return None.

    The data might not consistently cover consecutive days, but will be
    in order from oldest dates to most recent dates. Do not add daily weather
    for days where there is missing data (as defined in the handout). A "T"
    in the file indicates that there were trace values. Record trace values
    as -1 in the corresponding attribute.

    Preconditions:
        - f is open and is set to the beginning of the file.
        - The first line of f is a header, and the remaining lines
          follow the format specified in the handout.
        - There may be no lines of data, but there is at least a header.
    """
    lines = f.readlines()
    n = len(lines)
    if n == 1:
        return None
    line = lines[1].split(',')
    location = HistoricalWeather(line[STN_NAME].strip(' " '),
                                 (float(line[LAT].strip(' " ')),
                                  float(line[LONG].strip(' " '))))

    def check(values: list[str], n: int) -> bool:
        """Return true if all the values can be converted to int or float.

        >>> values = ['5']
        >>> n = len(values)
        >>> check(values, n)
        True
        """
        convert = True
        for x in range(n):
            if x < 3:
                try:
                    values[x] = int(values[x])
                except ValueError:
                    return False
            else:
                try:
                    values[x] = float(values[x])
                except ValueError:
                    return False
        return convert

    def precipflag(total_precip: str, total_precip_flag: str) -> float:
        """Determining if there were trace amounts of precipitation.

        >>> total_precip = "3"
        >>> total_precip_flag = ""
        >>> precipflag(total_precip, total_precip_flag)
        3
        """
        if total_precip_flag == "T":
            return -1
        try:
            total_precip = float(total_precip)
            return total_precip
        except ValueError:
            return -2

    def rainflag(total_rain: str, total_rain_flag: str) -> float:
        """Determining if there were trace amounts of rainfall.

        >>> rain = "3"
        >>> total_rain_flag = ""
        >>> precipflag(total_rain, total_rain_flag)
        3
        """
        if total_rain_flag == "T":
            return -1
        try:
            total_rain = float(total_rain)
            return total_rain
        except ValueError:
            return -2

    def snowflag(total_snow: str, total_snow_flag: str) -> float:
        """Determining if there were trace amounts of snowfall.

        >>> total_snow = "3"
        >>> total_snow_flag = ""
        >>> snowflag(total_snow, total_snow_flag)
        3
        """
        if total_snow_flag == "T":
            return -1
        try:
            total_snow = float(total_snow)
            return total_snow
        except ValueError:
            return -2

    for j in range(1, n):
        line = lines[j].split(',')
        line[YEAR] = line[YEAR].strip(' " ')
        line[MONTH] = line[MONTH].strip(' " ')
        line[DAY] = line[DAY].strip(' " ')
        line[MAX_TEMP] = line[MAX_TEMP].strip(' " ')
        line[MIN_TEMP] = line[MIN_TEMP].strip('"')
        line[MEAN_TEMP] = line[MEAN_TEMP].strip(' " ')
        line[TOTAL_RAIN] = line[TOTAL_RAIN].strip(' " ')
        line[TOTAL_RAIN_FLAG] = line[TOTAL_RAIN_FLAG].strip(' " ')
        line[TOTAL_SNOW] = line[TOTAL_SNOW].strip(' " ')
        line[TOTAL_SNOW_FLAG] = line[TOTAL_SNOW_FLAG].strip(' " ')
        line[TOTAL_PRECIP] = line[TOTAL_PRECIP].strip(' " ')
        line[TOTAL_PRECIP_FLAG] = line[TOTAL_PRECIP_FLAG].strip(' " ')
        values = [line[YEAR], line[MONTH], line[DAY], line[MAX_TEMP],
                  line[MIN_TEMP], line[MEAN_TEMP]]
        n = len(values)
        if check(values, n):
            precip = precipflag(line[TOTAL_PRECIP], line[TOTAL_PRECIP_FLAG])
            rain = rainflag(line[TOTAL_RAIN], line[TOTAL_RAIN_FLAG])
            snow = snowflag(line[TOTAL_SNOW], line[TOTAL_SNOW_FLAG])
            if precip != -2 and rain != -2 and snow != -2:
                weather = DailyWeather((float(line[MEAN_TEMP]),
                                        float(line[MIN_TEMP]), float
                                        (line[MAX_TEMP])), (precip, rain, snow))
                location.add_weather(date(int(line[YEAR]), int(line[MONTH]),
                                          int(line[DAY])), weather)
    return location


def load_country(folder_name: str, name: str) -> Country:
    """ Return a Country called name that contains all the historical weather
     data stored in the files that are in the folder called folder_name.

    Precondition:
    - Each file in the folder called folder_name:
        - is a .csv files that obeys the format specified in the handout
        - contains data for one location within this Country
    """
    country = Country(name)
    for filename in os.listdir(folder_name):
        # If there are any "dot files", ignore them.
        if not filename.startswith('.'):
            location_file = open(os.path.join(folder_name, filename), 'r')
            history = load_data(location_file)
            if history is not None:
                country.add_history(history)

    return country


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['load_country', 'generate_summary'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'datetime', 'os'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })

    import doctest
    doctest.testmod()

    # # Example use (1):
    # # Create weather day "by hand" and examine it using __str__ methods
    # # defined in the various classes.
    # weather_1 = DailyWeather((13, 9, 20), (5, 0, 0))
    # weather_2 = DailyWeather((14, 10, 21), (5, 0, 2.0))
    # canada = Country('Canada')
    # the_date = date(2020, 7, 13)
    # loc1_data = HistoricalWeather('Toronto', (43.6, -79.63))
    # loc1_data.add_weather(the_date, weather_1)
    # loc2_data = HistoricalWeather('YYZ', (43.6529, -79.3849))
    # loc2_data.add_weather(the_date - timedelta(1), weather_1)
    # loc2_data.add_weather(the_date + timedelta(1), weather_2)
    # canada.add_history(loc1_data)
    # canada.add_history(loc2_data)
    # # Try printing instances of each of the 3 classes.
    # print(f'----- a DailyWeather object:\n{weather_1}')
    # print(f'----- a HistoricalWeather object:\n{loc1_data}')
    # print(f'----- a Country object:\n{canada}')

    # # Example use (2):
    # # Load all the data in a folder, and generate a file "report.md"
    # # containing a simple summary of that data.
    # # Note: The file uses a format called "markdown", which includes
    # # special symbols describing desired formatting.  Open report.md in
    # # Pycharm, and it will show you a formatted version.
    canada = load_country('./student_data/', 'Canada')
    canada.generate_summary()
    print('bye')
