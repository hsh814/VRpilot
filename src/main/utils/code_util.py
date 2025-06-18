
def format_c_code(code):

    INDENT_SIZE = 4  # Number of spaces per indent level
    indent_level = 0
    formatted_code = ""
    lines = code.splitlines()

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespaces

        while '  ' in line:
            line = line.replace('  ', ' ')

        if line.startswith("#"):  # Preprocessor directive, no indentation
            formatted_code += line + "\n"
        else:
            if line.endswith("{"):  # Increase indent level for opening curly braces
                formatted_code += " " * (INDENT_SIZE * indent_level) + line + "\n"
                indent_level += 1
            elif line.startswith("}"):  # Decrease indent level for closing curly braces
                indent_level -= 1
                formatted_code += " " * (INDENT_SIZE * indent_level) + line + "\n"
            else:  # Normal line, use current indent level
                formatted_code += " " * (INDENT_SIZE * indent_level) + line + "\n"

    return formatted_code
