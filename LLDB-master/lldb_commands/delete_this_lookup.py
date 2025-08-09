

import lldb
import os
import argparse
import shlex

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
    'command script add -o -f delete_this_lookup.handle_command delete_this_lookup -h "Short documentation here"')

def handle_command(debugger, command, exe_ctx, result, internal_dict):
    '''
    Documentation for how to use delete_this_lookup goes here 
    '''

    command_args = command.split()
    parser = generate_option_parser()
    options = []
    args = []
    if len(command_args):
        try:
            args = parser.parse_args(command_args)
        except Exception as e:
            print("error were found")
            print(e)
            # result.SetError(e)
            return


    target = debugger.GetSelectedTarget()

    contextList = target.FindGlobalFunctions(args.searchstring, 0, lldb.eMatchTypeRegex)
    result.AppendMessage(str(contextList))


def generate_option_parser():
    usage = "usage: prog [options] TODO Description Here :]"
    parser = argparse.ArgumentParser(usage=usage, prog="delete_this_lookup")
    parser.add_argument("searchstring")
    parser.add_argument("-m", "--module",
                      action="store",
                      default=None,
                      dest="module",
                      help="This is a placeholder option to show you how to use options with strings")
    parser.add_argument("-c", "--check_if_true",
                      action="store_true",
                      default=False,
                      dest="store_true",
                      help="This is a placeholder option to show you how to use options with bools")
    return parser
    