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
    # Create empty array ot fill it with fields
    module_header_ready = []

    # Create module header
    module_header_ready.append("module {}".format(module['name']))

    # Create parameter section
    if(len(module['parameters']) != 0):
        module_header_ready.append('#')
        module_header_ready.append('(')

        for parameter_idx in range(len(module['parameters'])):
            param_type = module['parameters'][parameter_idx]['param_type']
            param_name = module['parameters'][parameter_idx]['param_name']
            param_value = module['parameters'][parameter_idx]['param_value']
            parameter_string = '\tparameter \t{} \t{} \t= {}'.format(param_type, param_name, param_value)

            if(parameter_idx != len(module['parameters']) - 1):
                parameter_string += ','

            module_header_ready.append(parameter_string)
        module_header_ready.append(')')
        module_header_ready.append('')


    # Create basic signals section
    module_header_ready.append('(')
    if(len(module['basic_signals']) != 0):
        module_header_ready.append('\t//Basic signals declaration')

        for basic_signal_idx in range(len(module['basic_signals'])):
            signal_direction = module['basic_signals'][basic_signal_idx]['signal_direction']
            signal_type = module['basic_signals'][basic_signal_idx]['signal_type']
            signal_width = module['basic_signals'][basic_signal_idx]['signal_width']
            signal_name = module['basic_signals'][basic_signal_idx]['signal_name']

            if(signal_width == '1'):
                singnal_string = '\t{} \t{} \t{} \t{}'.format(signal_direction, signal_type, '\t\t\t', signal_name)
            else:
                singnal_string = '\t{} \t{} \t[{}-1:0] \t\t{}'.format(signal_direction, signal_type, signal_width, signal_name)

            if(len(module['input_signals']) == 0) and (len(module['output_signals']) == 0) \
                and (len(module['inout_signals']) == 0) and (basic_signal_idx == len(module['basic_signals'])-1):
                print("Warning: module {} has no signals after basic ones".format(module['name']))
            else:
                singnal_string += ','

            module_header_ready.append(singnal_string)
        module_header_ready.append('')


    # Create input signals section
    if(len(module['input_signals']) != 0):
        module_header_ready.append('\t//Input signals signals declaration')

        for input_signal_idx in range(len(module['input_signals'])):
            signal_type = module['input_signals'][input_signal_idx]['signal_type']
            signal_width = module['input_signals'][input_signal_idx]['signal_width']
            signal_name = module['input_signals'][input_signal_idx]['signal_name']

            if(signal_width == '1'):
                singnal_string = '\t{} \t{} \t{} \t{}'.format('input', signal_type, '\t\t\t', signal_name)
            else:
                singnal_string = '\t{} \t{} \t[{}-1:0] \t\t{}'.format('input', signal_type, signal_width, signal_name)

            if(len(module['output_signals']) == 0) \
                and (len(module['inout_signals']) == 0) and (input_signal_idx == len(module['input_signals'])-1):
                print("Warning: module {} has no signals after basic ones".format(module['name']))
            else:
                singnal_string += ','

            module_header_ready.append(singnal_string)
        module_header_ready.append('')


        # Create output signals section
        if(len(module['output_signals']) != 0):
            module_header_ready.append('\t//Output signals signals declaration')

            for output_signal_idx in range(len(module['output_signals'])):
                signal_type = module['output_signals'][output_signal_idx]['signal_type']
                signal_width = module['output_signals'][output_signal_idx]['signal_width']
                signal_name = module['output_signals'][output_signal_idx]['signal_name']

                if(signal_width == '1'):
                    singnal_string = '\t{} \t{} \t{} \t{}'.format('output', signal_type, '\t\t\t', signal_name)
                else:
                    singnal_string = '\t{} \t{} \t[{}-1:0] \t\t{}'.format('output', signal_type, signal_width, signal_name)

                if(len(module['inout_signals']) == 0) and (output_signal_idx == len(module['output_signals'])-1):
                    print("Warning: module {} has no signals after input ones".format(module['name']))
                else:
                    singnal_string += ','

                module_header_ready.append(singnal_string)
            module_header_ready.append('')

    # Create inout signals section (WIP)

    # Create finish signals generation section
    module_header_ready.append(');')

    return module_header_ready


def create_module_local_variables(module):
    # Create empty array ot fill it with fields
    module_localvars_ready = []

    module_localvars_ready.append('')
    module_localvars_ready.append("//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    module_localvars_ready.append("//Begin of declaring local signals and parameters of {}'s module section".format(module['name']))
    module_localvars_ready.append('')

    # Create local parameter section
    if(len(module['localparams']) != 0):
        module_localvars_ready.append('//Declaring local parameters')
        module_localvars_ready.append('')

        for localparam_idx in range(len(module['localparams'])):
            localparam_type = module['localparams'][localparam_idx]['localparam_type']
            localparam_name = module['localparams'][localparam_idx]['localparam_name']
            localparam_value = module['localparams'][localparam_idx]['localparam_value']
            localparameter_string = 'localparam \t{} \t{} \t= {};'.format(localparam_type, localparam_name, localparam_value)

            module_localvars_ready.append(localparameter_string)
        module_localvars_ready.append('')

    # Create local parameter section
    if(len(module['internal_signals']) != 0):
        module_localvars_ready.append('//Declaring local signals')
        module_localvars_ready.append('')
    
        for internal_signal_idx in range(len(module['internal_signals'])):
            signal_type = module['internal_signals'][internal_signal_idx]['signal_type']
            signal_width = module['internal_signals'][internal_signal_idx]['signal_width']
            signal_name = module['internal_signals'][internal_signal_idx]['signal_name']

            if(signal_width == '1'):
                singnal_string = '{} \t{} \t{};'.format(signal_type, '\t\t\t', signal_name)
            else:
                singnal_string = '{} \t[{}-1:0] \t\t{};'.format(signal_type, signal_width, signal_name)
    
            module_localvars_ready.append(singnal_string)

        module_localvars_ready.append('')

    module_localvars_ready.append('')
    module_localvars_ready.append("//End of declaring local signals and parameters of {}'s module section".format(module['name']))
    module_localvars_ready.append("//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    module_localvars_ready.append('')

    return module_localvars_ready





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

                # Generating header
                module_header = create_module_header(module)
                print (module_header)
                for header_entry in module_header:
                    created_file.write(header_entry + "\n")

                # Generating local signals and parameters
                module_localvars = create_module_local_variables(module)
                print (module_header)
                for localvar_entry in module_localvars:
                    created_file.write(localvar_entry + "\n")

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