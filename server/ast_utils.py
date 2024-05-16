import ast


def assign_name(tree: ast.Assign):
    if len(tree.targets) != 1:
        return ""

    target = tree.targets[0]

    if not isinstance(target, ast.Name):
        return ""

    return target.id


def variable_is_name(tree: ast.Assign, name: str):
    return assign_name(tree) == name
