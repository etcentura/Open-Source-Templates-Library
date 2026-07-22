import os
import json
import argparse


module_localvars_template = [
    "//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv",
    "//Begin of declaring local signals and parameters of [module_name] module section",
    "//Internal constants",
    "localparam \t[localparam_type] \t[localparam_name] \t= [localparam_value];"
    "//Intenral signals"
    "\t[signal_type] \t[[singal_width]-1 : 0] \t[signal_name];",
    "//End of declaring local signals and parameters  of [common_module_template] module section",
    "//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
]


module_always_comb_template = [
    "always_comb",
    "begin",
    "\tsignal_name = value_to_assign;",
    "end"
]

module_assign_template = [
    "assign signal_name = value_to_assign;"
]

module_always_ff_rst_template = [
    "always_ff @(posedge clk or negedge rst_n)",
    "begin",
    "\tif(!rst_n)",
    "\t\tbegin",
    "\t\t\tsignal_name <= value_to_reset;",
    "\t\tend",
    "\telse",
    "\t\tbegin",
    "\t\t\tsignal_name <= value_to_assign;",
    "\t\tend",
    "end"
]

module_always_ff_norst_template = [
    "always_ff @(posedge clk)",
    "begin",
    "\tsignal_name <= value_to_assign;",
    "end"
]

def create_module_header(module):
    module_header_ready = []

    ports_counter = 0 
    for signal in module['signals']:
        if signal['signal_direction'] != 'internal':
            ports_counter += 1
    print("Number of ports found {}".format(ports_counter))
    
    module_header_ready.append("module {} #".format(module['name']))
    module_header_ready.append("(")
    
    for param_index, param in enumerate(module['parameters']):
        param_line = "\tparameter \t{} \t{} \t= {}".format(
            param['param_type'],
            param['param_name'],
            param['param_value']
        )
        if param_index != len(module['parameters']) - 1:
            param_line += ","
        module_header_ready.append(param_line)
    
    module_header_ready.append(")")
    module_header_ready.append("(")
    
    module_header_ready.append("\t //Basic ports declaration")
    module_header_ready.append("\tinput \tlogic \tclk,")
    module_header_ready.append("\tinput \tlogic \trst_n,")
    module_header_ready.append("")
    
    for signal_index, signal in enumerate(module['signals']):
        if signal['signal_direction'] != 'internal':
            if signal['signal_width'] == '1':
                port_line = "\t{} \t{} \t\t\t\t{}".format(
                    signal['signal_direction'],
                    signal['signal_type'],
                    signal['signal_name']
                )
            else:
                port_line = "\t{} \t{} \t[{}-1:0] \t{}".format(
                    signal['signal_direction'],
                    signal['signal_type'],
                    signal['signal_width'],
                    signal['signal_name']
                )
            
            remaining_ports = False
            for remaining_signal in module['signals'][signal_index+1:]:
                if remaining_signal['signal_direction'] != 'internal':
                    remaining_ports = True
                    break
            
            if remaining_ports:
                port_line += ","
            
            module_header_ready.append(port_line)
    
    module_header_ready.append(");")
    
    return module_header_ready





def parse_and_create(json_data):
    for module in json_data['modules']:
        print(">"*50)

        relative_path_to_place = module['path_to_place']
        absolute_path_to_place = os.path.abspath(relative_path_to_place)
        module_file_name = module['name'] + ".sv"
        full_path_to_module = absolute_path_to_place + "\\" + module_file_name

        print("Relative path is {}".format(relative_path_to_place))
        print("Absolute path is {}".format(absolute_path_to_place))
        print("File path is {}".format(module_file_name))
        print("Full path to module is {}".format(full_path_to_module))



        if (os.path.isdir(absolute_path_to_place)):
            print("Found {}.".format(absolute_path_to_place))
        else:
            print("Not found {}, creating the directory...".format(absolute_path_to_place))
            os.makedirs(module['path_to_place'])



        if(os.path.exists(full_path_to_module)):
            print("Found {}.".format(full_path_to_module))
        else:
            print("Not found {}, creating the file...".format(full_path_to_module))

            with open(full_path_to_module, 'w') as created_file:
                module_header = create_module_header(module)
                print (module_header)
                for header_entry in module_header:
                    created_file.write(header_entry + "\n")


        print("<"*50)
        print("\n")
    
        
        

# Creating main fucntion to parse args, etc.
def main():
    parser = argparse.ArgumentParser(
                                        prog='<<<Python template generator>>>',
                                        description='Generator creates the file (SV module or testbench) using the json type and name mentioned in call arguments.\n' \
                                        'If the required file is already created, you should handle one yourself, the generator will ignore the generation of created file.\n',
                                        epilog='Use it wisely and this will help you to save your time and protect you from boring modules writing :).'
                                     )
    
    parser.add_argument('-v', '--verbose', help='Verbose mode for the debugging purposes: Y for verbose', type=str, default='N')
    parser.add_argument('-json', help='Path to the json config file', type=str, default=None)

    args = parser.parse_args()

    if(args.verbose != 'Y') and (args.verbose != 'N'):
        parser.print_help()

    try:
        with open('{}'.format(args.json), 'r', encoding='utf-8') as config:

            if(args.verbose == 'Y'):
                print("Opening file : {}".format(config))

            data = json.load(config)

            parse_and_create(data)
            
    except FileNotFoundError:
        print("Error: The specified file {} does not exist.".format(args.json))

    


if __name__ == "__main__":
    main()