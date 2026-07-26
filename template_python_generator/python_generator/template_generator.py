import os
import json
import argparse

###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
# Global variables
section_begin_mark = "//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
section_end_mark = "//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"


###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
 
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
                signal_string = '\t{} \t{} \t{} \t{}'.format(signal_direction, signal_type, '\t\t\t', signal_name)
            else:
                signal_string = '\t{} \t{} \t[{}-1:0] \t\t{}'.format(signal_direction, signal_type, signal_width, signal_name)

            if(len(module['input_signals']) == 0) and (len(module['output_signals']) == 0) \
                and (len(module['inout_signals']) == 0) and (basic_signal_idx == len(module['basic_signals'])-1):
                print("Warning: module {} has no signals after basic ones".format(module['name']))
            else:
                signal_string += ','

            module_header_ready.append(signal_string)
        module_header_ready.append('')


    # Create input signals section
    if(len(module['input_signals']) != 0):
        module_header_ready.append('\t//Input signals signals declaration')

        for input_signal_idx in range(len(module['input_signals'])):
            signal_type = module['input_signals'][input_signal_idx]['signal_type']
            signal_width = module['input_signals'][input_signal_idx]['signal_width']
            signal_name = module['input_signals'][input_signal_idx]['signal_name']

            if(signal_width == '1'):
                signal_string = '\t{} \t{} \t{} \t{}'.format('input', signal_type, '\t\t\t', signal_name)
            else:
                signal_string = '\t{} \t{} \t[{}-1:0] \t\t{}'.format('input', signal_type, signal_width, signal_name)

            if(len(module['output_signals']) == 0) \
                and (len(module['inout_signals']) == 0) and (input_signal_idx == len(module['input_signals'])-1):
                print("Warning: module {} has no signals after basic ones".format(module['name']))
            else:
                signal_string += ','

            module_header_ready.append(signal_string)
        module_header_ready.append('')


        # Create output signals section
        if(len(module['output_signals']) != 0):
            module_header_ready.append('\t//Output signals signals declaration')

            for output_signal_idx in range(len(module['output_signals'])):
                signal_type = module['output_signals'][output_signal_idx]['signal_type']
                signal_width = module['output_signals'][output_signal_idx]['signal_width']
                signal_name = module['output_signals'][output_signal_idx]['signal_name']

                if(signal_width == '1'):
                    signal_string = '\t{} \t{} \t{} \t{}'.format('output', signal_type, '\t\t\t', signal_name)
                else:
                    signal_string = '\t{} \t{} \t[{}-1:0] \t\t{}'.format('output', signal_type, signal_width, signal_name)

                if(len(module['inout_signals']) == 0) and (output_signal_idx == len(module['output_signals'])-1):
                    print("Warning: module {} has no signals after input ones".format(module['name']))
                else:
                    signal_string += ','

                module_header_ready.append(signal_string)
            module_header_ready.append('')

    # Create inout signals section (WIP) #TODO

    # Create finish signals generation section
    module_header_ready.append(');')

    return module_header_ready


def create_module_local_variables(module):
    # Create empty array ot fill it with fields
    module_localvars_ready = []

    module_localvars_ready.append('')
    module_localvars_ready.append(section_begin_mark)
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

    # Create local sginals section
    if(len(module['internal_signals']) != 0):
        module_localvars_ready.append('//Declaring local signals')
        module_localvars_ready.append('')
    
        for internal_signal_idx in range(len(module['internal_signals'])):
            signal_type = module['internal_signals'][internal_signal_idx]['signal_type']
            signal_width = module['internal_signals'][internal_signal_idx]['signal_width']
            signal_name = module['internal_signals'][internal_signal_idx]['signal_name']

            if(signal_width == '1'):
                signal_string = '{} \t{} \t{};'.format(signal_type, '\t\t\t', signal_name)
            else:
                signal_string = '{} \t[{}-1:0] \t\t{};'.format(signal_type, signal_width, signal_name)
    
            module_localvars_ready.append(signal_string)

        module_localvars_ready.append('')

    module_localvars_ready.append('')
    module_localvars_ready.append("//End of declaring local signals and parameters of {}'s module section".format(module['name']))
    module_localvars_ready.append(section_end_mark)
    module_localvars_ready.append('')
    module_localvars_ready.append('endmodule')

    return module_localvars_ready

###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################

def create_testbench(testbench):
    # Create empty array ot fill it with fields
    testbench_ready = []
    testbench_ready.append("`timescale {}".format(testbench['timescale']))
    testbench_ready.append('')
    testbench_ready.append('module {}();'.format(testbench['name']))
    testbench_ready.append('')
    testbench_ready.append(section_begin_mark)
    testbench_ready.append('//Begin of declaring local signals and parameters of {} module section'.format(testbench["name"]))

    # Create module parameters section
    if(len(testbench['module_parameters']) != 0):
        testbench_ready.append('')
        testbench_ready.append('//Declaring module parameters')
        
        for param_idx in range(len(testbench['module_parameters'])):
            param_type = testbench['module_parameters'][param_idx]['param_type']
            param_name = testbench['module_parameters'][param_idx]['param_name']
            param_value = testbench['module_parameters'][param_idx]['param_value']
            parameter_string = '\tparameter \t{} \t{} \t= {};'.format(param_type, param_name, param_value)

            testbench_ready.append(parameter_string)
        testbench_ready.append('')

    # Create module signals section
    if(len(testbench['module_signals']) != 0):
        testbench_ready.append('')
        testbench_ready.append('//Declaring module singals')
        
        for signal_idx in range(len(testbench['module_signals'])):
            signal_type = testbench['module_signals'][signal_idx]['signal_type']
            signal_width = testbench['module_signals'][signal_idx]['signal_width']
            signal_name = testbench['module_signals'][signal_idx]['signal_name']
            
            if(signal_width == '1'):
                signal_string = '{} \t{} \t{};'.format(signal_type, '\t\t\t', signal_name)
            else:
                signal_string = '{} \t[{}-1:0] \t\t{};'.format(signal_type, signal_width, signal_name)
            
            testbench_ready.append(signal_string)
        testbench_ready.append('')

    # Create testbench parameters section
    if(len(testbench['testbench_parameters']) != 0):
        testbench_ready.append('')
        testbench_ready.append('//Declaring testbench parameters')
        for param_idx in range(len(testbench['testbench_parameters'])):
            param_type = testbench['testbench_parameters'][param_idx]['param_type']
            param_name = testbench['testbench_parameters'][param_idx]['param_name']
            param_value = testbench['testbench_parameters'][param_idx]['param_value']
            parameter_string = 'parameter \t{} \t{} \t= {};'.format(param_type, param_name, param_value)

            testbench_ready.append(parameter_string)
        testbench_ready.append('')

    # Create testbench singnals section (WIP) #TODO

    testbench_ready.append('//End of declaring local signals and parameters of {} module section'.format(testbench["name"]))
    testbench_ready.append(section_end_mark)
    testbench_ready.append('')


    # Declare module instance
    testbench_ready.append(section_begin_mark)
    testbench_ready.append('//Begin of instancing {} module section'.format(testbench["name"]))
    testbench_ready.append('')
    testbench_ready.append('{}'.format(testbench['name'].replace('tb_', '')))

    # Generating module parameters
    if(len(testbench['module_parameters']) != 0):
        testbench_ready.append('#')
        testbench_ready.append('(')

        for parameter_idx in range(len(testbench['module_parameters'])):
            param_name = testbench['module_parameters'][parameter_idx]['param_name']
            parameter_string = '\t.{} \t({})'.format(param_name, param_name)
        
            if(parameter_idx != len(testbench['module_parameters']) - 1):
                parameter_string += ','
        
            testbench_ready.append(parameter_string)
        
        testbench_ready.append(')')
        testbench_ready.append('')
    testbench_ready.append('')
    testbench_ready.append('i_{}'.format(testbench['name'].replace('tb_', '')))
    testbench_ready.append('(')

    # Generating module ports
    if(len(testbench['module_signals']) != 0):
        for signal_idx in range(len(testbench['module_signals'])):
            signal_name = testbench['module_signals'][signal_idx]['signal_name']
            signal_string = '\t.{} \t({})'.format(signal_name, signal_name)

            if(signal_idx != len(testbench['module_signals']) - 1):
                signal_string += ','
            
            testbench_ready.append(signal_string)
        testbench_ready.append('')
    testbench_ready.append(');')

    testbench_ready.append('//End of instancing {} module section'.format(testbench["name"]))
    testbench_ready.append(section_end_mark)

    # Generating clock driving
    if(len(testbench['clk_generation']) != 0):
        testbench_ready.append('')
        for clock_idx in range(len(testbench['clk_generation'])):
            clock_name = testbench['clk_generation'][clock_idx]['clk_name']
            clock_toggle_time = testbench['clk_generation'][clock_idx]['toggle']
            testbench_ready.append(section_begin_mark)
            testbench_ready.append('//Begin of generatring {} clock section'.format(clock_name))
            testbench_ready.append('')
            testbench_ready.append('initial')
            testbench_ready.append('begin : {}_generation_process'.format(clock_name))
            testbench_ready.append('\t{} = 0;'.format(clock_name))
            testbench_ready.append('\tforever #{} {}=~{};'.format(clock_toggle_time, clock_name, clock_name))
            testbench_ready.append('end')
            testbench_ready.append('')
            testbench_ready.append('//End of generatring {} clock section'.format(clock_name))
            testbench_ready.append(section_end_mark)

    testbench_ready.append(section_begin_mark)
    testbench_ready.append('//Begin of generatring main scenario section')
    testbench_ready.append('')
    testbench_ready.append('//End of generatring main scenario section')
    testbench_ready.append(section_end_mark)
    testbench_ready.append('')

    testbench_ready.append('endmodule')

    return testbench_ready


###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################

def parse_and_create(json_data):
    # Generate module
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
            if(module['overwrite'] == 'N'):
                print("Found {}, no file overwriting.".format(full_path_to_module))
        else:
            print("Not found or being overwritten: {}, creating the file...".format(full_path_to_module))

            with open(full_path_to_module, 'w') as created_file:

                # Generating header
                module_header = create_module_header(module)
                print (module_header)
                for header_entry in module_header:
                    created_file.write(header_entry + "\n")

                # Generating local signals and parameters
                module_localvars = create_module_local_variables(module)
                print (module_localvars)
                for localvar_entry in module_localvars:
                    created_file.write(localvar_entry + "\n")

        print("<"*50)
        print("\n")

    # Generate testbench
    for testbench in json_data['testbenches']:

        print(">"*50)
        
        relative_path_to_place = testbench['path_to_place']
        absolute_path_to_place = os.path.abspath(relative_path_to_place)
        testbench_file_name = testbench['name'] + ".sv"
        full_path_to_testbench = absolute_path_to_place + "\\" + testbench_file_name

        print("Relative path is {}".format(relative_path_to_place))
        print("Absolute path is {}".format(absolute_path_to_place))
        print("File path is {}".format(testbench_file_name))
        print("Full path to module is {}".format(full_path_to_testbench))

        if (os.path.isdir(absolute_path_to_place)):
            print("Found {}".format(absolute_path_to_place))
        else:
            print("Not found {}, creating the directory...".format(absolute_path_to_place))
            os.makedirs(testbench['path_to_place'])

        if(os.path.exists(full_path_to_testbench)):
            if(module['overwrite'] == 'N'):
                print("Found {}, no file overwriting.".format(full_path_to_testbench))
        else:
            print("Not found  or being overwritten: {}, creating the file...".format(full_path_to_testbench))
        
            with open(full_path_to_testbench, 'w') as created_file:
                    
                # Generating testbench
                testbench_header = create_testbench(testbench)
                print(testbench_header)
                for testbench_entry in testbench_header:
                    created_file.write(testbench_entry + "\n")
        
        print("<"*50)
        print("\n")
        
###################################################################################################################################################      
###################################################################################################################################################      
###################################################################################################################################################      

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
