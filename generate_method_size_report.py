#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import subprocess

def parseArgs():
    import argparse
    description = "Lists all functions with their object file path and size"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'file',
        help='Unstripped binary file')
    parser.add_argument(
        'output',
        help='Where we save the output in JSON format')
    parser.add_argument(
        '--at-least',
        help='Defines the lower size of method to find',
        type=int,
        default=0)
    parser.add_argument(
        '--at-most',
        help='Defines the upper size of method to find',
        type=int,
        default=1457664)
        
    return parser.parse_args()

def runWithArgs(args):
    # Ищем строки вида "OSO /path/to/file.o", "OSO /path/to/liba.a(file.o)"
    process = subprocess.Popen("nm -a {} | grep -o \"OSO .*\" | cut -c 5-".format(args.file), shell=True, stdout=subprocess.PIPE)
    
    oso_entries = []
    for line in iter(process.stdout.readline, b''):
        line = line.strip()
        oso_entries.append(line)
        
    result = []
    
    for entry in oso_entries:
        # Выводит кучу данных, нас интересует самая первая таблица вида
        #            0x0000abcd [0x0STARTADD - 0x0ENDADDR) methodName
        # Из этих строк мы вытаскиваем начальный и конечный адреса и methodName
        process = subprocess.Popen("dwarfdump -a \"{}\" | grep \"0x.*: \\[0x.* - 0x.*) .*\" | grep -o \"\\[.*\"".format(entry), shell=True, stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            line = line.strip()
            line_parts = line.split(' ')                  # line - вида "[0x0STARTADD - 0x0ENDADDR) methodName"
            start_address = int(line_parts[0][1:], 16)    # `1:`  - первый символ [, мы его игнорируем
            end_address = int(line_parts[2][:-1], 16)     # `:-1` - последний символ ), мы его игнорируем 
            method_size = end_address - start_address 
            if method_size >= args.at_least and method_size <= args.at_most:
                method_name = line_parts[3]
                result_entry = {"object_file": entry, "method_name": method_name, "method_size": method_size}
                print(str(result_entry))
                result.append(result_entry)
    
    with open(args.output, 'w') as output:
        json.dump(result, output)
    
def main():
    args = parseArgs()
    runWithArgs(args)

if __name__ == '__main__':
    main()
