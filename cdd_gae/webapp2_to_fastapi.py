"""
'Upgrade' WebApp2 to FastAPI with this shiny function
"""


def webapp2_to_fastapi(mod):
    """
    Convert WebApp2 to FastAPI

    :param mod: AST module containing WebApp2 routes and mapper function call
    :type mod: ```ast.Module```

    :returns: Equivalent AST module but for FastAPI
    :rtype: ```ast.Module```
    """
    if mod.body:
        raise NotImplementedError
    return mod


__all__ = ["webapp2_to_fastapi"]
