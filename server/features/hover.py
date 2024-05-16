from typing import Optional
from lsprotocol.types import HoverParams, Hover as HoverResponse, Position, Range
from pygls.server import LanguageServer
from variables import VariablesList


class Hover:
    def __init__(self, params: HoverParams, server: LanguageServer, variables: VariablesList) -> None:
        self.params = params
        self.server = server
        self.variables = variables
        self.document = self.server.workspace.get_text_document(self.params.text_document.uri)
        self.word = self.document.word_at_position(self.params.position)

    def hover(self) -> Optional[HoverResponse]:
        var = self.variables.find(self.word)

        if var is None:
            return

        return HoverResponse(var.documentation(), range=self._range())

    def _range(self):
        line = self._line()

        word_len = len(self.word)

        char_num = self.params.position.character
        start = line.find(self.word, max(char_num - word_len, 0), min(char_num + word_len, len(line) - 1))

        end = start + word_len

        line_num = self.params.position.line

        return Range(Position(line_num, start), Position(line_num, end))

    def _line(self):
        return self.document.lines[self.params.position.line]
