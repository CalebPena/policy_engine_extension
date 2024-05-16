import * as path from 'path';

const folderName = path.basename(__dirname);
export const EXTENSION_ROOT_DIR =
    folderName === 'common' ? path.dirname(path.dirname(__dirname)) : path.dirname(__dirname);
export const BUNDLED_PYTHON_SCRIPTS_DIR = path.join(EXTENSION_ROOT_DIR, 'server');
export const SERVER_SCRIPT_PATH = path.join(BUNDLED_PYTHON_SCRIPTS_DIR, 'server.py');
export const DEBUG_SERVER_SCRIPT_PATH = path.join(BUNDLED_PYTHON_SCRIPTS_DIR, '_debug_server.py');
