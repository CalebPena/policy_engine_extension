from typing import Optional
from lsprotocol.types import Location, MarkupContent, MarkupKind, Position, Range
import ast
from ast_utils import variable_is_name


class Variable:
    LABEL_NAME = "label"
    VALUE_TYPE_NAME = "value_type"
    ENTITY_NAME = "entity"
    PERIOD_NAME = "definition_period"

    BASE_NAME = "Variable"

    class NotAVariableException(Exception):
        pass

    def __init__(
        self,
        name: str,
        location: Location,
        label: Optional[str] = None,
        value_type: Optional[str] = None,
        entity: Optional[str] = None,
        period: Optional[str] = None,
    ) -> None:
        self.name = name
        self.label = label
        self.value_type = value_type
        self.entity = entity
        self.period = period
        self.location = location

    @classmethod
    def from_ast(cls, uri: str, source: str, tree: ast.ClassDef):
        """
        turn class tree into variable
        """
        name: str = tree.name

        if not cls._is_variable(tree):
            raise cls.NotAVariableException(f"{name} is not a variable")

        location = Location(uri, Range(Position(tree.lineno - 1, tree.col_offset), Position(tree.lineno - 1, tree.col_offset)))
        label: Optional[str] = None
        value_type: Optional[str] = None
        entity: Optional[str] = None
        period: Optional[str] = None

        for node in tree.body:
            if isinstance(node, ast.Assign):
                if variable_is_name(node, cls.LABEL_NAME):
                    label = ast.get_source_segment(source, node.value)
                if variable_is_name(node, cls.VALUE_TYPE_NAME):
                    value_type = ast.get_source_segment(source, node.value)
                if variable_is_name(node, cls.ENTITY_NAME):
                    entity = ast.get_source_segment(source, node.value)
                if variable_is_name(node, cls.PERIOD_NAME):
                    period = ast.get_source_segment(source, node.value)

        return Variable(
            name,
            location,
            label=label,
            value_type=value_type,
            entity=entity,
            period=period,
        )

    @classmethod
    def _is_variable(cls, tree: ast.ClassDef) -> bool:
        for base in tree.bases:
            if not isinstance(base, ast.Name):
                continue

            if base.id == "Variable":
                return True

        return False

    def documentation(self) -> MarkupContent:
        """
        documentation for the variable
        """
        pad = "  "
        label = f"{pad}{self.LABEL_NAME} = {self.label}" if self.label else ""
        value_type = f"{pad}{self.VALUE_TYPE_NAME} = {self.value_type}" if self.value_type else ""
        entity = f"{pad}{self.ENTITY_NAME} = {self.entity}" if self.entity else ""
        period = f"{pad}{self.PERIOD_NAME} = {self.period}" if self.period else ""

        body = "\n".join([v for v in [label, value_type, entity, period] if v != ""])
        if body == "":
            body = f"{pad}pass"

        value = f"""
```python
class {self.name}({self.BASE_NAME}):
{body}
```
        """
        return MarkupContent(kind=MarkupKind.Markdown, value=value)

    def __repr__(self) -> str:
        items = [f"location = {self.location}"]

        if self.label:
            items.append(f"label = {self.label}")
        if self.value_type:
            items.append(f"value_type = {self.value_type}")
        if self.entity:
            items.append(f"entity = {self.entity}")
        if self.period:
            items.append(f"period = {self.period}")

        return f"{self.name}(" + "".join(["\n\t" + item for item in items]) + "\n)"


class VariablesList(dict[str, list[Variable]]):
    def find(self, name: str) -> Optional[Variable]:
        """
        find the variable by name
        """
        for var in self.variables():
            if var.name == name:
                return var

    def update(self, uri: str, source: str):
        """
        update variables from a file
        """
        try:
            tree = ast.parse(source=source)
        except SyntaxError:
            return

        self._remove_var_from_uri(uri)

        module_vars: list[Variable] = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                try:
                    var = Variable.from_ast(uri, source, node)
                    module_vars.append(var)
                except Variable.NotAVariableException:
                    pass

        self[uri] = module_vars

    def _remove_var_from_uri(self, uri: str):
        if uri not in self:
            return

        del self[uri]

    def variables(self):
        """
        iterate over all of the variables
        """
        for file in self.values():
            for variable in file:
                yield variable
