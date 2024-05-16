from typing import Optional
from lsprotocol.types import DefinitionParams, Location
from pygls.server import LanguageServer
from variables import VariablesList


class Definition:
    def __init__(self, params: DefinitionParams, server: LanguageServer, variables: VariablesList) -> None:
        self.params = params
        self.server = server
        self.variables = variables
        self.document = self.server.workspace.get_text_document(self.params.text_document.uri)
        self.word = self.document.word_at_position(self.params.position)

    def definition(self) -> Optional[Location]:
        var = self.variables.find(self.word)

        if var is None:
            return

        return var.location
