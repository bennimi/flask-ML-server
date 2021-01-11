$("#fileinput-form").click(function(){
    
    /*$.validator.setDefaults({
        errorClass: 'help-block',
        highlight: function(element) {
          $(element)
            .closest('.form-group')
            .addClass('has-error');
        },
        unhighlight: function(element) {
          $(element)
            .closest('.form-group')
            .removeClass('has-error');
        }
      });*/ 

    $.validator.addMethod( "extension", function( value, element, param ) {
    	param = typeof param === "string" ? param.replace( /,/g, "|" ) : "csv|txt";
    	return this.optional( element ) || value.match( new RegExp( "\\.(" + param + ")$", "i" ) );
    }, $.validator.format( "Please enter a file with a valid extension." ) )

    $("#fileinput-form").validate({
          onfocusout: function(e) {  // this option is not needed
                this.element(e);       // this is the default behavior
          },
          rules:{
              inputfile: {
              required: true,
              extension: true
              }
          },
          messages:{
              inputfile:{
              required: "Please input a file."
              }
          },
    
     });

});

$("#fileinput-form").on("change",function(e) { 
     console.log('file changed'); 
     $("#fileinput-form").trigger('blur');
     /*$("hidden-input").focus();*/
});