module [common_module_template]
//Begin of declaring [common_module_template]'s parameters
#
(
parameter	[param_type]	[param_name]	=	[param_value],
)
//End of declaring [common_module_template]'s parameters


//Begin of declaring [common_module_template]'s singals
(
    //Basic signals declaration begin
    input		logic		                                                clk                 ,
    input		logic		                                                rst_n               ,
    //Basic signals declaration end
    
    //Data signals declaration begin
    [singal_direction]		[signal_type]		[[singal_width]-1 : 0] 	    [signal_name]       ,
    //Data signals declaration end
);
//End of declaring [common_module_template]'s singals



//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of declaring [common_module_template]'s functions section

function int fucntion_template (input int argument);
begin
    
end    
endfunction

//End of declaring [common_module_template]'s functions  section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of declaring local signals and parameters of [common_module_template] module section

//Internal constants
localparam      int      [my_local_parameter]       =   ;

//Intenral signals
[signal_type]		[[singal_width]-1 : 0] 	    [signal_name]       ,

//End of declaring local signals and parameters  of [common_module_template] module section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of driving [signal_name] via combinational driver section

always_comb
begin
    signal_name = value_to_assign;
end

assign signal_name = value_to_assign;

//End of driving [signal_name] via combinational driver section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of driving [signal_name] via sequential driver section

always_ff @(posedge clk or negedge rst_n)
begin
    if(!rst_n)
        begin
            signal_name <= value_to_reset;
        end
    else
        begin
            signal_name <= value_to_assign;
        end
end

always_ff @(posedge clk)
begin
    signal_name <= value_to_assign;
end

//End of driving [signal_name] via sequential driver section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
endmodule