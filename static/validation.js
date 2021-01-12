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
    	param = typeof param === "string" ? param.replace( /,/g, "|" ) : "" ;
    	return this.optional( element ) || value.match( new RegExp( "\\.(" + param + ")$", "i" ) );
    });

    $.validator.addMethod( "maxsize", function( value, element, param ) {
	if ( this.optional( element ) ) {
		return true;
	}

	if ( $( element ).attr( "type" ) === "file" ) {
		if ( element.files && element.files.length ) {
			for ( var i = 0; i < element.files.length; i++ ) {
				if ( element.files[ i ].size > param ) {
					return false;
				}
			}
		}
	}
	return true;
    });

    $("#fileinput-form").validate({
          onfocusout: function(e) {  
                this.element(e);       
          },
          rules:{
              inputfile: {
              required: true,
              extension: "txt,csv",
              maxsize: 0.1 * 1024 * 1024
              }
          },
          messages:{
              inputfile:{
              required: "Please input a file.",
              extension: $.validator.format("Please input a valid file extension {0}."),
              maxsize: $.validator.format("Please input a file no more than {0} bytes.")
              }
          },
    
     });

});

/*
$("#fileinput-form").on("change",function(e) { 
     console.log('file changed'); 
     $("#fileinput-form").trigger('blur');
     $("hidden-input").focus();
});
*/
