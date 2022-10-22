"""
Mocks for NDB
"""
from ast import ClassDef, Name, Assign, Load, Store, keyword, Call, Attribute

from cdd.ast_utils import set_value

ndb_file_cls_str = """
class File(FileBase):
    updated = ndb.DateTimeProperty(auto_now=True, indexed=False)

    used_at = ndb.DateTimeProperty(indexed=True)
    archived = ndb.BooleanProperty(default=False, indexed=True)
    archived_at = ndb.DateTimeProperty(indexed=False)

    path_source = ndb.StringProperty(indexed=True)
    source = ndb.TextProperty()  # For files ingested from external libraries
"""

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
            lineno=None 
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
            lineno=None
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
            lineno=None
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
            lineno=None
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
            lineno=None
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
            lineno=None
        ),
    ],
    decorator_list=[],
)

__all__ = ["ndb_file_cls", "ndb_file_cls_str"]
