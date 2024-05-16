from typing import Optional
from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
)
from pygls.server import LanguageServer
from features.snippets import python_snippets, yaml_snippets
from variables import VariablesList


class Completion:
    def __init__(self, params: CompletionParams, server: LanguageServer, variables: VariablesList) -> None:
        self.params = params
        self.server = server
        self.variables = variables
        self.document = self.server.workspace.get_text_document(self.params.text_document.uri)

    def completion(self) -> Optional[CompletionList]:
        if self.document.language_id == "python":
            return self.python_completion()
        if self.document.language_id == "yaml":
            return self.yaml_completion()

    def python_completion(self) -> Optional[CompletionList]:
        completion_list = python_snippets

        if self._in_python_string():
            completion_list += tuple(self._variable_completions())

        return CompletionList(
            False,
            completion_list,
        )

    def yaml_completion(self) -> Optional[CompletionList]:
        completion_list = yaml_snippets

        if self._should_yaml_complete():
            completion_list += tuple(self._variable_completions())

        return CompletionList(
            False,
            completion_list,
        )

    def _in_python_string(self) -> bool:
        line = self._line()
        cur_char_pos = self.params.position.character

        # check the current character, the 2 characters before
        char_range = slice(max(cur_char_pos - 3, 0), min(cur_char_pos, len(line)))

        chars = line[char_range]

        return ('"' in chars) or ("'" in chars)

    def _should_yaml_complete(self) -> bool:
        line = self._line()[: max(self.params.position.character - 2, 0)]
        # only return completions if the line is empty or contains only a "-"
        if line.strip() in ("", "-"):
            return True

        return False

    def _variable_completions(self) -> list[CompletionItem]:
        items: list[CompletionItem] = []

        for var in self.variables.variables():
            item = CompletionItem(
                var.name, insert_text=var.name, documentation=var.documentation(), kind=CompletionItemKind.Variable
            )
            items.append(item)

        return items

    def _line(self) -> str:
        return self.document.lines[self.params.position.line]
