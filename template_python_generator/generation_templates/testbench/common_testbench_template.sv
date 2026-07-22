//Begin of generating timescale of [tb_jpeg_top_module] testbench
`timescale 1ns/1ps
//End of generating timescale of [tb_jpeg_top_module] testbench

module [common_testbench_template] ();

//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of declaring local signals and parameters of [common_module_template] module section

//Internal constants
localparam      int      [my_local_parameter]       =           ;

//Intenral signals
logic		            [internal_signal_single]                ;
logic		[0 : 0] 	[internal_signal_bus]                   ;

//File processing variables
int                     [file_name_descriptor]                  ;
string                  [file_path_variable] = [path_to_file]   ;

//End of declaring local signals and parameters of [common_module_template] module section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of instancing [common_testbench_template]'s dut section

[dut_name] 
#
(
    
)
            i_[dut_name]
(
    
);

endmodule

//End of instancing [common_testbench_template]'s dut section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of [common_testbench_template]'s clock generation section



//End of [common_testbench_template]'s clock generation section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of [common_testbench_template]'s task generation section

task task_tempalte(arguments);
begin
    
end
endtask

//End of [common_testbench_template]'s task generation section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of [common_testbench_template]'s file processing section
initial begin : file_processing
    file_name_descriptor = $fopen(file_path_variable, "__x__");
end

final begin
    $fclose();
end
//End of [common_testbench_template]'s file processing section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of [common_testbench_template]'s main scenario section

initial begin: main
    
end

//End of [common_testbench_template]'s main scenario section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
endmodule