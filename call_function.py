import json
from config import WORKING_DIR
from functions.get_file_content import get_file_content, get_file_content_tool
from functions.run_python_file import run_python_file, run_python_file_tool
from functions.write_file import write_file, write_file_tool
from functions.get_files_info import get_files_info, get_files_info_tool

tools = [
    get_files_info_tool,
    get_file_content_tool,
    run_python_file_tool,
    write_file_tool,
]

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call, verbose=False):
    function_name = function_call.function.name or ""
    function_args = json.loads(function_call.function.arguments)
    tool_call_id = function_call.id

    if verbose:
        print(f"f - Calling function {function_name}({function_args})")
    else:
        print(f"f - Calling function {function_name}")

    if function_name not in function_map:
        return {
            "tool_call_id": tool_call_id,
            "role": "tool",
            "name": function_name,
            "content": f"error: unknown function: {function_name}",
        }

    args = dict(function_args) if function_args else {}
    args["working_directory"] = WORKING_DIR
    result = function_map[function_name](**args)

    return {
        "tool_call_id": tool_call_id,
        "role": "tool",
        "name": function_name,
        "content": result,
    }
