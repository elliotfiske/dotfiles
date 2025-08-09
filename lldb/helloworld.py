import os
import time

def test_loop(debugger, command, result, dict):
    print(f'lldb pid is: {os.getpid()}')


def __lldb_init_module(debugger, dict):
    module = os.path.splitext(os.path.basename(__file__))[0]
    function = test_loop.__name__
    print(f'\nRegistering {module}.{function}. Call "{function}" from lldb to run the script')
    debugger.HandleCommand(f'command script add -f {module}.{function} {function}')
    print(f'\nAttach to lldb at: {os.getpid()}. Remember to use the "unsigned_lldb" in ~/lldb/')