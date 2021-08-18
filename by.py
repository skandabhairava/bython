import sys, os

def main(args: list):
    without_file_args = ["--help", "-h"]
    execute = False
    execute_statement = ""

    try:
        system_arguments = args
    except Exception as e:
        raise RuntimeError(e)

    if len(system_arguments) <= 1:
        raise RuntimeError("Doesn't contain any arguments")
    
    file_location = str(system_arguments[1])

    if not os.path.exists(file_location):
        if not file_location in without_file_args:
            raise FileNotFoundError(f"file '{file_location}' doesn't exist!")
        print("Without File Arguments : \n--help -h : help menu\n\nFile arguments : \n--execute -e <command to run> to auto execute the file")
        sys.exit(1)
    else:
        file_location = os.path.abspath(file_location)
        if ("--execute" in system_arguments or "-e" in system_arguments):
            if len(system_arguments) >= 4:
                execute_statement = system_arguments[3]
                execute = True
            else:
                raise RuntimeError("no execution argument given")        

    if file_location[-3:] != ".by":
        raise ImportError(f"Can only convert a '*.by' file, cannot convert {file_location}")
    
    with open(file_location, "r") as file:
        file_content = file.read()

    file_name = f'{file_location[:-3]}.py'

    #print(file_content.replace("\n\n", "&\n").split("\n"))
    #converted_code = file_content.replace(";\n", "\n").replace(";", "\n").replace("<\n", ":\n").replace("<", ":\n").replace(">\n", "").replace(">", "\n")
    converted_code = _convert(_split_multiple(file_content, [";", "<", ">"]))

    with open(file_name , "w") as save_file:
        save_file.write(converted_code)
        print(f"File generated at : {file_name}")

    if execute:
        os.system(f"{execute_statement} {file_name}")

def _convert(file_content:list) -> str:
    """
    file_content:list -> a list of lines, which is run by the program
    file_name:str -> name of the file
    """
    spacing:str = "    "
    space = 4
    block:int = 0
    line_count = 0
    python_code = "# File Generated using bython\n"
    for line in file_content:
        if line[-1] == "<":
            #print("'" + line + "'")
            for char in line[::-1][1:]:
                if not char in [" ", "\n", "\t"]:
                    python_code += spacing * block + line[:line.rfind(char) +1 ] + ":" + "\n"
                    #print(line[:line.rfind(char)])
                    break
                
            block += 1
        elif line[-1] == ">":
            python_code += line[:-1]
            block -= 1
            if block == 0:
                python_code += "\n"
        elif line[-1] == ";":
            python_code += spacing * block + line[:-1] + "\n"
            ...
        else:
            python_code += spacing * block + line + "\n"
        #python_code += line[:-1] + "\n"
        if block < 0:
            raise RuntimeError("A bracket hasn't been exited/closed")
        line_count += 1
    return python_code

def _split_multiple(text:str, list_char:list) -> list:
    sub_text = ""
    return_list = []
    for char_num in range(len(text)):
        char = text[char_num]
        sub_text += char
        if char in list_char:
            try:
                if text[char_num - 1] != "\\":
                    return_list.append(sub_text.strip())
                    sub_text = ""
            except IndexError:
                return_list.append(sub_text.strip())
                sub_text = ""
        if char == "\\" and text[char_num + 1] in list_char:
                    sub_text = sub_text[:-1]

    return return_list

if __name__ == "__main__":
    main(sys.argv)