"""
Parquet parser utils
"""


def parquet_type_to_param(pyarrow_wrap_data_type):
    """
    pyarrow_wrap_data_type
    """
    return {"typ": str(pyarrow_wrap_data_type)}


__all__ = ["parquet_type_to_param"]
