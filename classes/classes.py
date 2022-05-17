'''
Here goes the defined classes for the project.
None are yet to be defined, but a categorical to numerical conversion for some features may be implemented here using the enum librrary.

Affected features: KosherType, cook_time, prep_ease, prep_time, scaling.
'''

from enum import Enum


class KosherType(str, Enum):
    parve = "parve"
    milchik = "milchik"
    fleisch = "fleisch"
    nonkosher = "nonkosher"
    #kosher      ::: kosher type [parve|milchik|fleisch]
