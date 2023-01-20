"""
Parquet parser utils
"""

from itertools import chain
from operator import attrgetter

import pyarrow
from pyarrow import DataType, ListType, StructType, TimestampType


def union_or_scalar(iterable):
    """
    Create `Union[str,int]` or `str` depending on length of input

    :param iterable: Tuple or List (or similar) with size known ahead of time containing strings
    :type iterable: ```Iterable[str]```

    :return: `Union[str,int]` or `str` depending on length of input
    :rtype: ```str```
    """
    return iterable[0] if len(iterable) == 1 else "Union[{}]".format(",".join(iterable))


def parquet_type_to_param(field):
    """
    Convert Parquet type to param

    :param field: PyArrow field
    :type field: ```pyarrow.lib.Field```

    :return: {"typ": <parsed_type_as_str>}
    :rtype: ```dict```
    """
    field_type = field.type
    if isinstance(field_type, TimestampType):
        return {"typ": str(field_type)}
    elif isinstance(field_type, StructType):
        return {
            "typ": list(map(lambda flattened: str(flattened.type), field.flatten()))
        }
    elif isinstance(field_type, ListType):
        reduction = field_type.__reduce__()
        assert len(reduction) > 1
        assert reduction[0] == pyarrow.lib.list_
        return {
            "typ": union_or_scalar(
                tuple(
                    chain.from_iterable(
                        map(
                            lambda t: map(str, map(attrgetter("type"), t)),
                            reduction[1:],
                        )
                    )
                )
            )
        }
    elif isinstance(field_type, DataType):
        return {
            "typ": union_or_scalar(
                tuple(map(lambda flattened: str(flattened.type), field.flatten()))
            )
        }
    else:
        raise NotImplementedError(field_type)


__all__ = ["parquet_type_to_param"]
