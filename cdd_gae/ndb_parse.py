"""
Parse NDB `class`es
"""


def parse_ndb(python_file, dry_run):
    """
    Parse NDB

    :param dry_run: Show what would be created; don't actually write to the filesystem
    :type dry_run: ```bool```

    :param python_file: Python source file path
    :type python_file: ```str```
    """
    if dry_run:
        print("[parse_ndb] Dry running")
    raise NotImplementedError("parse_ndb(python_file={})".format(python_file))


__all__ = ["parse_ndb"]
