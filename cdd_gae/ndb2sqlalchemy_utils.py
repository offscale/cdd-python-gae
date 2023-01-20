"""
Module that holds a utility dict for parses NDB types and emits SQLalchemy types/constraints
"""

from ast import Attribute, Call, Load, Name, Tuple

from cdd.ast_utils import get_value

ndb2sqlalchemy_params = {"indexed": "index"}


def ndb_to_sqlalchemy_keyword(keyword):
    """
    Convert per column NDB calls to SQLalchemy calls

    :param keyword: AST keyword
    :type keyword: ```keyword```

    :return: keyword key, keyword value
    :rtype: ```Tuple[str, AST]```
    """
    if keyword.arg in ndb2sqlalchemy_params:
        return ndb2sqlalchemy_params[keyword.arg], keyword.value
    elif keyword.arg == "auto_now_add" and get_value(keyword.value) is True:
        return "server_default", Call(
            args=[], func=Name(ctx=Load(), id="utcnow"), keywords=[]
        )
    elif keyword.arg == "auto_now":
        return "onupdate", Call(
            func=Attribute(
                value=Name(id="func", ctx=Load()), attr="utc_timestamp", ctx=Load()
            ),
            args=[],
            keywords=[],
        )
    elif keyword.arg == "choices":
        # TODO: Get enum to work
        # return "default", get_value(keyword.value.elts[0])
        return "type_", Call(
            func=Name(id="Enum", ctx=Load()),
            args=[
                Tuple(
                    ctx=Load(),
                    elts=keyword.value.elts,
                    expr=None,
                )
            ],
            keywords=[],
        )
    elif keyword.arg == "repeated":
        return (
            "doc",
            "TODO: Maybe with `ARRAY` type?"
            " https://cloud.google.com/appengine/docs/legacy/standard/python/ndb/entity-property-reference#repeated",
        )
    # else:
    #     print(ast.dump(keyword.value, indent=4))
    return keyword.arg, keyword.value


__all__ = ["ndb2sqlalchemy_params"]
