from urllib.parse import urlparse, unquote
import os
import pathlib
import fnmatch
import sys


def update_sys_path(path_to_add: str, strategy: str) -> None:
    """Add given path to `sys.path`."""
    if path_to_add not in sys.path and os.path.isdir(path_to_add):
        if strategy == "useBundled":
            sys.path.insert(0, path_to_add)
        elif strategy == "fromEnvironment":
            sys.path.append(path_to_add)


# Ensure that we can import LSP libraries, and other bundled libraries.
update_sys_path(
    os.fspath(pathlib.Path(__file__).parent / "libs"),
    os.getenv("LS_IMPORT_STRATEGY", "useBundled"),
)


from pygls.server import LanguageServer
from lsprotocol.types import (
    INITIALIZE,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DEFINITION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_HOVER,
    CompletionOptions,
    CompletionParams,
    DefinitionParams,
    DidChangeTextDocumentParams,
    HoverParams,
    InitializeParams,
    TextDocumentSyncKind,
)
from dotenv import load_dotenv
from features.definition import Definition
from features.hover import Hover
from variables import VariablesList
from features.completion import Completion


load_dotenv()
try:
    debug = os.environ["DEBUG"] == "True"
except KeyError:
    debug = False

server = LanguageServer("policy_engine", "v0.1", text_document_sync_kind=TextDocumentSyncKind.Full)

variables = VariablesList()


def should_ignore(ignore_list: list[str], path: str):
    for ignore in ignore_list:
        if fnmatch.fnmatch(path, ignore):
            return True

    return False


def get_all_variables_in_dir(root_dir: str):
    ignore_files: list[str] = []
    try:
        with open(os.path.join(root_dir, ".gitignore"), "r") as f:
            lines = f.readlines()
            ignore_files = [l.strip() for l in lines if not l.startswith("#") and l != "\n"]
    except FileNotFoundError:
        pass

    for subdir, dir, files in os.walk(root_dir):
        dir[:] = [d for d in dir if not should_ignore(ignore_files, os.path.relpath(os.path.join(subdir, d), root_dir))]

        for file in files:
            if not file.endswith(".py"):
                continue

            path = pathlib.Path(os.path.join(subdir, file))
            relpath = os.path.relpath(path, root_dir)

            if should_ignore(ignore_files, relpath):
                continue

            with path.open() as f:
                try:
                    text = f.read()
                except:
                    continue

            uri = path.as_uri()
            variables.update(uri, text)


def pathify(uri: str):
    path_components = urlparse(uri).path.split("/")
    path = os.path.join(*path_components)
    return pathlib.Path(unquote(path)).absolute()


@server.feature(INITIALIZE)
def initialize(params: InitializeParams):
    server.send_notification("error", "no workspace selected")
    if params.workspace_folders is None:
        if params.root_uri is not None:
            get_all_variables_in_dir(pathify(params.root_uri))
        return

    for folder in params.workspace_folders:
        get_all_variables_in_dir(pathify(folder.uri))


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def text_document_change(params: DidChangeTextDocumentParams):
    variables.update(params.text_document.uri, params.content_changes[0].text)


@server.feature(TEXT_DOCUMENT_COMPLETION, options=CompletionOptions(trigger_characters=["-", '"', "'"]))
def completions(params: CompletionParams):
    return Completion(params, server, variables).completion()


@server.feature(TEXT_DOCUMENT_DEFINITION)
def definitions(params: DefinitionParams):
    return Definition(params, server, variables).definition()


@server.feature(TEXT_DOCUMENT_HOVER)
def hover(params: HoverParams):
    return Hover(params, server, variables).hover()


if debug:
    server.start_tcp("127.0.0.1", 9090)
else:
    server.start_io()
