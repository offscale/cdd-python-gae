"""
Mocks for NDB
"""
from ast import Assign, Attribute, Call, ClassDef, Load, Name, Store, keyword
from collections import OrderedDict

from cdd.ast_utils import maybe_type_comment, set_value

ndb_file_cls_str = """
class File(FileBase):
    updated = ndb.DateTimeProperty(auto_now=True, indexed=False)

    used_at = ndb.DateTimeProperty(indexed=True)
    archived = ndb.BooleanProperty(default=False, indexed=True)
    archived_at = ndb.DateTimeProperty(indexed=False)

    path_source = ndb.StringProperty(indexed=True)
    source = ndb.TextProperty()  # For files ingested from external libraries
"""


ndb_file_ir = {
    "doc": "",
    "name": "File",
    "params": OrderedDict(
        (
            (
                "updated",
                {
                    "doc": "",
                    "typ": "str",
                    "x_typ": {
                        "internal_type": "ndb.DateTimeProperty",
                        "sql": {
                            "constraints": {"auto_now": True, "indexed": False},
                            "type": "DateTime",
                        },
                    },
                },
            ),
            (
                "used_at",
                {
                    "doc": "",
                    "typ": "str",
                    "x_typ": {
                        "internal_type": "ndb.DateTimeProperty",
                        "sql": {"constraints": {"indexed": True}, "type": "DateTime"},
                    },
                },
            ),
            (
                "archived",
                {
                    "default": False,
                    "doc": "",
                    "typ": "bool",
                    "x_typ": {
                        "internal_type": "ndb.BooleanProperty",
                        "sql": {"constraints": {"indexed": True}, "type": "Boolean"},
                    },
                },
            ),
            (
                "archived_at",
                {
                    "doc": "",
                    "typ": "str",
                    "x_typ": {
                        "internal_type": "ndb.DateTimeProperty",
                        "sql": {"constraints": {"indexed": False}, "type": "DateTime"},
                    },
                },
            ),
            (
                "path_source",
                {
                    "doc": "",
                    "typ": "str",
                    "x_typ": {
                        "sql": {"constraints": {"indexed": True}, "type": "String"}
                    },
                },
            ),
            (
                "source",
                {
                    "doc": "",
                    "typ": "str",
                    "x_typ": {
                        "internal_type": "ndb.TextProperty",
                        "sql": {"type": "Text"},
                    },
                },
            ),
        )
    ),
    "returns": None,
    "type": "static",
}

ndb_file_cls = ClassDef(
    name="File",
    bases=[Name(id="FileBase", ctx=Load())],
    keywords=[],
    body=[
        Assign(
            targets=[Name(id="updated", ctx=Store())],
            value=Call(
                func=Attribute(
                    value=Name(id="ndb", ctx=Load()),
                    attr="DateTimeProperty",
                    ctx=Load(),
                ),
                args=[],
                keywords=[
                    keyword(arg="auto_now", value=set_value(True)),
                    keyword(arg="indexed", value=set_value(False)),
                ],
            ),
            expr=None,
            lineno=None,
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(id="used_at", ctx=Store())],
            value=Call(
                func=Attribute(
                    value=Name(id="ndb", ctx=Load()),
                    attr="DateTimeProperty",
                    ctx=Load(),
                ),
                args=[],
                keywords=[keyword(arg="indexed", value=set_value(True))],
            ),
            expr=None,
            lineno=None,
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(id="archived", ctx=Store())],
            value=Call(
                func=Attribute(
                    value=Name(id="ndb", ctx=Load()), attr="BooleanProperty", ctx=Load()
                ),
                args=[],
                keywords=[
                    keyword(arg="default", value=set_value(False)),
                    keyword(arg="indexed", value=set_value(True)),
                ],
            ),
            expr=None,
            lineno=None,
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(id="archived_at", ctx=Store())],
            value=Call(
                func=Attribute(
                    value=Name(id="ndb", ctx=Load()),
                    attr="DateTimeProperty",
                    ctx=Load(),
                ),
                args=[],
                keywords=[keyword(arg="indexed", value=set_value(False))],
            ),
            expr=None,
            lineno=None,
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(id="path_source", ctx=Store())],
            value=Call(
                func=Attribute(
                    value=Name(id="ndb", ctx=Load()), attr="StringProperty", ctx=Load()
                ),
                args=[],
                keywords=[keyword(arg="indexed", value=set_value(True))],
            ),
            expr=None,
            lineno=None,
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(id="source", ctx=Store())],
            value=Call(
                func=Attribute(
                    value=Name(id="ndb", ctx=Load()), attr="TextProperty", ctx=Load()
                ),
                args=[],
                keywords=[],
            ),
            expr=None,
            lineno=None,
            **maybe_type_comment
        ),
    ],
    decorator_list=[],
)

ndb_file_sqlalchemy_cls = ClassDef(
    bases=[Name(ctx=Load(), id="Base")],
    body=[
        Assign(
            targets=[Name(ctx=Store(), id="__tablename__")],
            value=set_value("File"),
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(ctx=Store(), id="updated")],
            value=Call(
                args=[Name(ctx=Load(), id="DateTime")],
                func=Name(ctx=Load(), id="Column"),
                keywords=[
                    keyword(arg="auto_now", value=set_value(True)),
                    keyword(arg="indexed", value=set_value(False)),
                ],
            ),
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(ctx=Store(), id="used_at")],
            value=Call(
                args=[Name(ctx=Load(), id="DateTime")],
                func=Name(ctx=Load(), id="Column"),
                keywords=[keyword(arg="indexed", value=set_value(True))],
            ),
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(ctx=Store(), id="archived")],
            value=Call(
                args=[Name(ctx=Load(), id="Boolean")],
                func=Name(ctx=Load(), id="Column"),
                keywords=[
                    keyword(arg="indexed", value=set_value(True)),
                    keyword(arg="default", value=set_value(False)),
                    keyword(arg="nullable", value=set_value(False)),
                ],
            ),
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(ctx=Store(), id="archived_at")],
            value=Call(
                args=[Name(ctx=Load(), id="DateTime")],
                func=Name(ctx=Load(), id="Column"),
                keywords=[keyword(arg="indexed", value=set_value(False))],
            ),
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(ctx=Store(), id="path_source")],
            value=Call(
                args=[Name(ctx=Load(), id="String")],
                func=Name(ctx=Load(), id="Column"),
                keywords=[keyword(arg="indexed", value=set_value(True))],
            ),
            **maybe_type_comment
        ),
        Assign(
            targets=[Name(ctx=Store(), id="source")],
            value=Call(
                args=[Name(ctx=Load(), id="Text")],
                func=Name(ctx=Load(), id="Column"),
                keywords=[],
            ),
            **maybe_type_comment
        ),
    ],
    decorator_list=[],
    keywords=[],
    name="File",
)

__all__ = ["ndb_file_cls", "ndb_file_cls_str", "ndb_file_ir", "ndb_file_sqlalchemy_cls"]
