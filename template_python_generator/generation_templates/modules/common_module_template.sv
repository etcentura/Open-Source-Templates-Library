module [common_module_template]
//Begin of declaring [common_module_template]'sparameters
#
(
    parameter		[my_parameter]		=	,
)
//End of declaring [common_module_template]'s parameters


//Begin of declaring [common_module_template]'s singals
(
    //Basic signals declaration begin
    input		logic		            clk                     ,
    input		logic		            rst_n                   ,
    //Basic signals declaration end
    
    //Input signals declaration begin
    input		logic		            [in_port_single]        ,
    input		logic		[0 : 0] 	[in_port_bus]           ,
    //Input signals declaration end

    //Output signals
    output		logic		            [out_port_single]       ,
    output		logic		[0 : 0] 	[out_port_bus]          ,
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
logic		            [internal_signal_single]        ;
logic		[0 : 0] 	[internal_signal_bus]           ;

//End of declaring local signals and parameters  of [common_module_template] module section
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



//vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//Begin of driving [signal_name] via combinational driver section

always_comb
begin
    signal_name = value_to_assign;
end

assign [signal_name] = value_to_assign;

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