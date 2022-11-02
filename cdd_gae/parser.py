"""
Parsers for cdd GAE
"""

from ast import Assign, Attribute, Call, ClassDef, get_docstring, parse
from collections import OrderedDict

from cdd_gae.parser_utils import ndb_parse_assign


def ndb(source):
    """
    Parse NDB into the cdd IR

    :param source: Python source code for NDB class
    :type source: ```str```

    :return: a dictionary of form
        {  "name": Optional[str],
           "type": Optional[str],
           "doc": Optional[str],
           "params": OrderedDict[str, {'typ': str, 'doc': Optional[str], 'default': Any}]
           "returns": Optional[OrderedDict[Literal['return_type'],
                                           {'typ': str, 'doc': Optional[str], 'default': Any}),)]] }
    :rtype: ```dict```
    """
    assert isinstance(source, str)
    mod = parse(source)
    assert isinstance(mod.body[0], ClassDef)
    return ndb_class_def(mod.body[0])


def ndb_class_def(ndb_cls_def):
    """
    Parse NDB—from ast.ClassDef—into the cdd IR

    :param ndb_cls_def: `ast.ClassDef` of NDB class
    :type ndb_cls_def: ```ast.ClassDef```

    :return: a dictionary of form
        {  "name": Optional[str],
           "type": Optional[str],
           "doc": Optional[str],
           "params": OrderedDict[str, {'typ': str, 'doc': Optional[str], 'default': Any}]
           "returns": Optional[OrderedDict[Literal['return_type'],
                                           {'typ': str, 'doc': Optional[str], 'default': Any}),)]] }
    :rtype: ```dict```
    """
    assert isinstance(ndb_cls_def, ClassDef)
    return {
        "name": ndb_cls_def.name,
        "doc": get_docstring(ndb_cls_def) or "",
        "params": OrderedDict(
            (node.targets[0].id, ndb_parse_assign(node))
            for node in ndb_cls_def.body
            if isinstance(node, Assign)
            and isinstance(node.value, Call)
            and isinstance(node.value.func, Attribute)
            and node.value.func.value.id == "ndb"
        ),
        "returns": None,
        "type": "static",
    }


__all__ = ["ndb", "ndb_class_def"]
