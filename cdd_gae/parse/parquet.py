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

    :param source: ParquetFile, str, pathlib.Path, pyarrow.NativeFile, or file-like object
        Readable source.
    :type source: ```Union[ParquetFile,str,pathlib.Path,pyarrow.NativeFile,Readable]```
    """
    is_parquet_file = isinstance(source, ParquetFile)
    parquet_file = source if is_parquet_file else ParquetFile(source)
    return {
        "name": None
        if is_parquet_file or not path.isfile(source)
        else path.basename(source),
        "params": OrderedDict(
            (
                (
                    name,
                    parquet_type_to_param(parquet_file.schema_arrow.field(name)),
                )
                for name in parquet_file.schema_arrow.names
            )
        ),
        "returns": None,
    }


__all__ = ["parquet"]
