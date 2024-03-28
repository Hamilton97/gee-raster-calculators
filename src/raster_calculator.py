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

    @staticmethod
    def calculate_savi(
        nir: str, red: str, l: float = 0.5, name: str = None
    ) -> Callable:
        """
        Calculates the Soil-Adjusted Vegetation Index (SAVI) for a given image.

        Args:
            nir (str): The name of the Near Infrared (NIR) band.
            red (str): The name of the Red band.
            l (float, optional): The SAVI coefficient. Defaults to 0.5.
            name (str, optional): The name of the output band. Defaults to "SAVI".

        Returns:
            Callable: A function that calculates the SAVI for a given image.

        Example:
            savi_calculator = calculate_savi("B8", "B4", l=0.5)
            savi_image = savi_calculator(image)
        """
        name = name or "SAVI"
        return lambda x: x.addBands(
            x.expression(
                "(1 + L) * (NIR - RED) / (NIR + RED + L)",
                {
                    "NIR": x.select(nir),
                    "RED": x.select(red),
                    "L": l,
                },
            ).rename(name)
        )

    @staticmethod
    def calculate_tasseled_cap(*bands) -> Callable:
        g, b, r, nir, swir1, swir2 = bands

        def wrapper(image: ee.Image) -> ee.Image:
            tmp_img = image.select(g, b, r, nir, swir1, swir2)
            co_array = [
                [0.3037, 0.2793, 0.4743, 0.5585, 0.5082, 0.1863],
                [-0.2848, -0.2435, -0.5436, 0.7243, 0.0840, -0.1800],
                [0.1509, 0.1973, 0.3279, 0.3406, -0.7112, -0.4572],
            ]

            co = ee.Array(co_array)

            arrayImage1D = tmp_img.toArray()
            arrayImage2D = arrayImage1D.toArray(1)

            components_image = (
                ee.Image(co)
                .matrixMultiply(arrayImage2D)
                .arrayProject([0])
                .arrayFlatten([["brightness", "greenness", "wetness"]])
            )

            return image.addBands(components_image)

        return wrapper
