"""
Parquet file to python_cdd IR
"""
from collections import OrderedDict
from os import path

from pyarrow.parquet import ParquetFile

from cdd_gae.parse.parquet_utils import parquet_type_to_param


def parquet(source):
    """
    Parse parquet file into python_cdd IR

    :param source: str, pathlib.Path, pyarrow.NativeFile, or file-like object
        Readable source.
    :type source: ```Union[str,pathlib.Path,pyarrow.NativeFile,Readable]```
    """
    parquet_file = ParquetFile(source)
    return {
        "name": path.basename(source) if path.isfile(source) else None,
        "params": OrderedDict(
            (
                (
                    name,
                    parquet_type_to_param(parquet_file.schema_arrow.field(name)),
                )
                for name in parquet_file.schema_arrow.names
            )
        ),
        "return": None,
    }


__all__ = ["parquet"]
