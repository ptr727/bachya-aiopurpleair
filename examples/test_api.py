"""Run an example script to quickly test."""

import asyncio
import logging
from typing import Final

from aiohttp import ClientSession

from aiopurpleair import API
from aiopurpleair.errors import PurpleAirError

_LOGGER = logging.getLogger()

API_KEY: Final[str] = "API_READ_KEY"
READ_KEYS: Final[list[str] | None] = None
INDEXES: Final[list[int] | None] = None
LATITUDE: Final[float] = 51.5285582
LONGITUDE: Final[float] = -0.2416796
DISTANCE: Final[float] = 10
LIMIT: Final[int | None] = 10
FIELDS: Final[list[str]] = [
    "0.3_um_count",
    "0.5_um_count",
    "1.0_um_count",
    "10.0_um_count",
    "2.5_um_count",
    "5.0_um_count",
    "altitude",
    "firmware_version",
    "hardware",
    "humidity",
    "latitude",
    "location_type",
    "longitude",
    "model",
    "name",
    "pm1.0",
    "pm10.0",
    "pm2.5",
    "pressure",
    "rssi",
    "temperature",
    "uptime",
    "voc",
]


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            api = API(API_KEY, session=session)

            sensors_response = await api.sensors.async_get_sensors(
                fields=FIELDS, read_keys=READ_KEYS, sensor_indices=INDEXES
            )
            _LOGGER.info(sensors_response)

            nearby_sensor_indices = await api.sensors.async_get_nearby_sensors(
                fields=FIELDS,
                latitude=LATITUDE,
                longitude=LONGITUDE,
                distance_km=DISTANCE,
                limit_results=LIMIT,
                read_keys=READ_KEYS,
            )
            _LOGGER.info(nearby_sensor_indices)
        except PurpleAirError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
