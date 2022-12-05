from datagarden.helpers import GeoAPI, coordinates_to_geojson_point
from timezonefinder import TimezoneFinder


class LocationCommandsMixin(object):
    def get_coordinates(self):
        """
        returns the coordinates for an addressed composed of zip_code, city,
        iso3116_country_code and a list of address fields.
        """
        zip_code_key = self.process_args.get('zip_code_key', None)
        city_key = self.process_args.get('city_name_key', None)
        country_code_key = self.process_args.get('country_code', None)
        # migrate to useage of 'iso3116_country_code' arg
        country_code_key = country_code_key or self.process_args.get(
            'iso3116_country_code', None)

        zip_code = self._get_field(zip_code_key)
        city = self._get_field(city_key)
        country_code = self._get_field(country_code_key)

        address_keys = self.process_args.get('address_keys', [])
        address = ''.join(list(filter(
            None, [self._get_field(key) for key in address_keys])))
        address_items = [address, zip_code, city, country_code]
        address_items = [item for item in address_items
                         if isinstance(item, str)]
        return GeoAPI().get_geojson_point_from_address(','.join(address_items))

    def get_time_zone_from_coordinates(self):
        """Returns timezone from a specific GeoJson point
        """
        lat_field = self.process_args.get('lat', None)
        lon_field = self.process_args.get('lon', None)
        lat = self._get_field(lat_field)
        lon = self._get_field(lon_field)

        if not (lat and lon):
            return None

        return TimezoneFinder().timezone_at(lng=lon, lat=lat)
