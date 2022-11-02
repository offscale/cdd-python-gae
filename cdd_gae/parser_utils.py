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

ndb2sqlalchemy_types = {
    "BlobKeyProperty": "str",
    "BlobProperty": "str",
    "BooleanProperty": "Boolean",
    "ComputedProperty": "str",
    "DateProperty": "Date",
    "DateTimeProperty": "DateTime",
    "FloatProperty": "Float",
    "GenericProperty": "str",
    "GeoPtProperty": "str",
    "IndexProperty": "str",
    "IntegerProperty": "Integer",
    "JsonProperty": "JSON",
    "KeyProperty": "str",
    "LocalStructuredProperty": "str",
    "PickleProperty": "PickleType",
    "Property": "str",
    "StringProperty": "String",
    "StructuredProperty": "str",
    "TextProperty": "Text",
    "TimeProperty": "Time",
    "UserProperty": "UserDefinedType",
}


def ndb_parse_assign(assign):
    """
    Parse out the `ast.Assign` into an IR param. This always makes an SQL column representation.

    :param assign: NDB assignment, like `prop = ndb.BooleanProperty()`
    :type assign: ```ast.Assign```

    :return: a dictionary of form
        { 'typ': str, 'x_typ': {'sql': {'type': str, 'constraints': Dict}},
          'doc': Optional[str], 'default': Any }
    :rtype: ```dict```
    """
    ir = {
        "doc": "",
        "typ": ndb_type_map[assign.value.func.attr],
        "x_typ": {
            "sql": {
                "constraints": {
                    keyword.arg: get_value(keyword.value)
                    for keyword in assign.value.keywords
                },
                # "type": assign.value.func.attr
            }
            if assign.value.keywords
            else {}
        },
    }
    if "default" in ir["x_typ"].get("sql", {}).get("constraints", ()):
        ir["default"] = ir["x_typ"]["sql"]["constraints"].pop("default")
    internal_type = ".".join((assign.value.func.value.id, assign.value.func.attr))

    ir["x_typ"]["sql"]["type"] = ndb2sqlalchemy_types[assign.value.func.attr]

    if internal_type not in frozenset(
        ("ndb.StringProperty", "ndb.IntegerProperty", "ndb.FloatProperty")
    ):
        ir["x_typ"]["internal_type"] = internal_type
    return ir


__all__ = ["ndb_parse_assign"]
