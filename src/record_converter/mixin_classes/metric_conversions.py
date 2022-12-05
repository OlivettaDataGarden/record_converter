"""Module to define MetricsCommandsMixin
"""

class MetricsCommandsMixin(object):
    """
    Mixin class to extent CommandClass with metrics conversion methods.

    methods:
        - knots_to_km_per_hour
        - knots_to_meter_per_second
    """

    def knots_to_km_per_hour(self) -> float:
        """converts knots to km per hour"""
        wind_speed_in_knots_key = self.process_args
        wind_speed_in_knots = self._get_field(
            wind_speed_in_knots_key)
        return round(float(wind_speed_in_knots) * 1.853, 2)

    def knots_to_meter_per_second(self) -> float:
        """converts knots to meter per second"""
        wind_speed_in_knots_key = self.process_args
        wind_speed_in_knots = self._get_field(
            wind_speed_in_knots_key)
        return round(float(wind_speed_in_knots) * 0.514444, 2)
