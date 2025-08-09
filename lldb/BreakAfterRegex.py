import lldb
import optparse
import shlex


def breakAfterRegex(debugger, command, result, internal_dict):
    command = command.replace('\\', '\\\\')
    command_args = shlex.split(command, posix=False)
    parser = generateOptionParser()

    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return

    target = debugger.GetSelectedTarget()

    clean_command = shlex.split(args[0])[0]

    if options.non_regex:
        breakpoint = target.BreakpointCreateByName(clean_command, options.module)
    else:
        breakpoint = target.BreakpointCreateByRegex(clean_command, options.module)

    if not breakpoint.IsValid() or breakpoint.num_locations == 0:
        result.AppendWarning("Breakpoint isn't valid or hasn't found any hits")
    else:
        result.AppendMessage("{}".format(breakpoint))

    breakpoint.SetScriptCallbackFunction("BreakAfterRegex.breakpointHandler")


def breakpointHandler(frame, bp_loc, dict):
    '''The function called when the regular expression breakpoint gets triggered'''

    thread = frame.GetThread()
    process = thread.GetProcess()
    debugger = process.GetTarget().GetDebugger()

    function_name = frame.GetFunctionName()

    debugger.SetAsync(False)

    thread.StepOut()

    output = evaluateReturnedObject(debugger, thread, function_name)

    if output is not None:
        print(output)
    else:
        print("Could not figure out function's return value.")

    return False


def evaluateReturnedObject(debugger, thread, function_name):
    ''''Grabs the reference from the return register and returns a string from the evaluated value. TODO: currently objc only'''

    res = lldb.SBCommandReturnObject()

    interpreter = debugger.GetCommandInterpreter()
    target = debugger.GetSelectedTarget()
    frame = thread.GetSelectedFrame()
    parent_function_name = frame.GetFunctionName()

    expression = 'expression -lobjc -O -- $arg1'

    interpreter.HandleCommand(expression, res)

    if res.HasResult():
        output = '{}\nbreakpoint: ' \
                 '{}\nobject: {}\nstopped: {}'.format('*' * 80, function_name, res.GetOutput().replace('\n', ''),
                                                      parent_function_name)
        return output
    else:
        return "error: " + res.GetError()


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f BreakAfterRegex.breakAfterRegex bar')


def generateOptionParser():
    ''''Gets the return register as a string for lldb based upon the hardware'''
    usage = "usage: %prog [options] breakpoint_query\nUse 'bar -h' for option desc"

    parser = optparse.OptionParser(usage=usage, prog='bar')
    parser.add_option('-n', "--non_regex",
                      action="store_true",
                      default=False,
                      dest="non_regex",
                      help="Use a non-regex breakpoint instead")

    parser.add_option("-m", "--module",
                      action="store",
                      default=None,
                      dest="module",
                      help="Filter a breakpoint by only searching within a specified Module")

    return parser
