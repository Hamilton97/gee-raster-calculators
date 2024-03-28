from typing import Callable
import ee


class RasterCalculator:
    def __init__(self) -> None:
        ee.Initialize()

    @staticmethod
    def calculate_ndvi(nir: str, red: str, name: str = None) -> Callable:
        """
        Calculates the Normalized Difference Vegetation Index (NDVI) for a given pair of bands.

        Parameters:
            nir (str): The name of the Near Infrared (NIR) band.
            red (str): The name of the Red band.
            name (str, optional): The name to assign to the calculated NDVI band. Defaults to "NDVI".

        Returns:
            Callable: A function that calculates the NDVI for a given image.

        Example:
            calculate_ndvi("B4", "B3") returns a function that calculates the NDVI for an image using the bands "B4" (NIR) and "B3" (Red).
        """
        name = name or "NDVI"
        return lambda x: x.addBands(x.normalizedDifference([nir, red]).rename(name))
