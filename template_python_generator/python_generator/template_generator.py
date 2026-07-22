import os
import json
import argparse

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
                with open("../generation_templates/modules/common_module_template.sv") as template_file:

                    #Declaring flag to mark up the required fields
                    generation_markup = False

                    #Finding and replacing name of the module
                    for line in template_file:
                        if line.startswith("module"):
                            captured_line = line
                            replaced_line = captured_line.replace("[common_module_template]", module['name'])
                            created_file.write(replaced_line)
                            break
                    
                    #Find and replace parameters in the template module
                    generation_markup = False
                    for line in template_file:
                        if(line.startswith("//Begin of declaring [common_module_template]'s parameters")):
                            generation_markup = True
                            continue
                        elif(line.startswith("//End of declaring [common_module_template]'s parameters")):
                            generation_markup = False
                            break
                        elif(generation_markup):
                            if(("[param_type]" in line) and ("[param_name]" in line) and ("[param_value]" in line)):
                                for param_num in range(len(module['parameters'])):
                                    captured_line = line
                                    captured_line = captured_line.replace("[param_type]",   module['parameters'][param_num]['param_type'])
                                    captured_line = captured_line.replace("[param_name]",   module['parameters'][param_num]['param_name'])
                                    captured_line = captured_line.replace("[param_value]",  module['parameters'][param_num]['param_value'])

                                    #Checking on the last parameter for the correct comma placement
                                    if(param_num == len(module['parameters'])-1):
                                        captured_line = captured_line.replace(',','')

                                    created_file.write("{}".format(captured_line))
                            else:
                                created_file.write("{}".format(line))

                    #Find and replace parameters in the template module
                    generation_markup = False

                    ports_counter = 0
                    for signal_num in range(len(module['signals'])):
                        if (module['signals'][signal_num]['signal_direction'] != 'internal'):
                            ports_counter += 1

                    for line in template_file:
                        if(line.startswith("Begin of declaring ports of")):
                            generation_markup = True
                            continue

                        elif(line.startswith("End of declaring ports of")):
                            generation_markup = False
                            break
                        
                        elif(generation_markup):
                            if(("[singal_direction]" in line) and ("[signal_type]" in line) and ("[singal_width]" in line) and ("[signal_name]" in line)):
                                for signal_num in range(ports_counter):
                                    captured_line = line

                                    captured_line = captured_line.replace("[singal_direction]", module['signals'][signal_num]['signal_direction'])
                                    captured_line = captured_line.replace("[signal_type]", module['signals'][signal_num]['signal_type'])

                                    captured_line = captured_line.replace("[singal_width]", str(module['signals'][signal_num]['signal_width']))

                                    if(module['signals'][signal_num]['signal_width'] != '1'):
                                        captured_line = captured_line.replace("[singal_width]", str(module['signals'][signal_num]['signal_width']))
                                    else:
                                        captured_line = captured_line.replace("[[singal_width]-1 : 0]", "\t\t")

                                    captured_line = captured_line.replace("[signal_name]", module['signals'][signal_num]['signal_name'])

                                    #Checking on the last parameter for the correct comma placement
                                    if(signal_num == ports_counter - 1):
                                        captured_line = captured_line.replace(',','')

                                    created_file.write("{}".format(captured_line))
                            else:
                                created_file.write("{}".format(line))

                    #Find and insert functions template if some of them exist
                    generation_markup = False
                    if(len(module['functions']) != 0):
                        #TODO - create fucntion generation (WIP)
                        print("Functions insert is WIP section of generator") 

                    #Find and insert all localparams and internal signals
                    for line in template_file:
                        if(line.startswith("Begin of declaring local signals")):
                            temp_line = line
                            temp_line = temp_line.replace("[common_module_template]", module['name'])
                            created_file.write("{}".format(line))
                            generation_markup = True
                            continue
                        
                        elif(line.startswith("End of declaring local signals")):
                            temp_line = line
                            temp_line = temp_line.replace("[common_module_template]", module['name'])
                            created_file.write("{}".format(line))
                            generation_markup = False
                            break

                        elif(generation_markup):
                            if((len(module['localparams'])) != 0):
                                #TODO - create fucntion generation (WIP)
                                print("Functions insert is WIP section of generator")

                            if(("[signal_type]" in line) and ("[singal_width]" in line) and ("[signal_name]" in line)):
                                for signal_num in range(len(module['signals'])):

                                    if(module['signals'][signal_num]['signal_direction'] == 'internal'):
                                        captured_line = line
                                        captured_line = captured_line.replace("[signal_type]", module['signals'][signal_num]['signal_type'])

                                        if(module['signals'][signal_num]['signal_width'] != '1'):
                                            captured_line = captured_line.replace("[singal_width]", str(module['signals'][signal_num]['signal_width']))
                                        else:
                                            captured_line = captured_line.replace("[[singal_width]-1 : 0]", "\t\t")
                                        
                                        captured_line = captured_line.replace("[signal_name]", module['signals'][signal_num]['signal_name'])

                                        created_file.write("{}".format(captured_line))
                            else:
                                created_file.write("{}".format(line))

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