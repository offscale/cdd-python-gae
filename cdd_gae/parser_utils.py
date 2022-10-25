"""
Utils for parser.py
"""
from cdd.ast_utils import get_value

ndb_type_map = {
    "BlobKeyProperty": "str",
    "BlobProperty": "str",
    "BooleanProperty": "bool",
    "ComputedProperty": "str",
    "DateProperty": "str",
    "DateTimeProperty": "str",
    "FloatProperty": "float",
    "GenericProperty": "str",
    "GeoPtProperty": "str",
    "IndexProperty": "str",
    "IntegerProperty": "int",
    "JsonProperty": "str",
    "KeyProperty": "str",
    "LocalStructuredProperty": "str",
    "PickleProperty": "str",
    "Property": "str",
    "StringProperty": "str",
    "StructuredProperty": "str",
    "TextProperty": "str",
    "TimeProperty": "str",
    "UserProperty": "str",
}


def ndb_parse_assign(assign):
    """
    Parse out the `ast.Assign` into an IR param

    :param assign: NDB assignment, like `prop = ndb.BooleanProperty()`
    :type assign: ```ast.Assign```

    :return: a dictionary of form
        {'typ': str, 'doc': Optional[str], 'default': Any}
    :rtype: ```dict```
    """
    ir = {
        "typ": ndb_type_map[assign.value.func.attr],
        "x_typ": {
            keyword.arg: get_value(keyword.value) for keyword in assign.value.keywords
        },
    }
    if "default" in ir["x_typ"]:
        ir["default"] = ir["x_typ"].pop("default")
    internal_type = ".".join((assign.value.func.value.id, assign.value.func.attr))
    if internal_type not in frozenset(
        ("ndb.StringType", "ndb.IntegerProperty", "ndb.FloatProperty")
    ):
        ir["x_typ"]["internal_type"] = internal_type
    return ir


__all__ = ["ndb_parse_assign"]
