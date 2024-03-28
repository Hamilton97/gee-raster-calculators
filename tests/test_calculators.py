import pytest
import ee

from raster_calculator import RasterCalculator

ee.Initialize()


def test_ndvi_calc():
    calc = RasterCalculator.calculate_ndvi("NIR", "RED")
    img = ee.Image([1, 2]).rename(["NIR", "RED"])
    actual = calc(img).select("NDVI").bandNames().getInfo()
    expected = ["NDVI"]
    assert expected == actual


def test_ndvi_calc_collection():
    calc = RasterCalculator.calculate_ndvi("NIR", "RED")
    collection = ee.ImageCollection(
        [ee.Image([1, 2]).rename(["NIR", "RED"]) for _ in range(1, 4)]
    ).map(calc)

    collection.select("NDVI").getInfo()
