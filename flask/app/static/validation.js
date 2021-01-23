$("#fileinput-form").change(function(){
    
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
         showErrors: function(errorMap, errorList) {
                // Do nothing here
          },
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


$("#inputfile").bind("change",function(){
   var filesize = this.files[0].size;
   var filename = this.files[0].name;
   var x = "";
   console.log(filesize);
   console.log(filename);

   fetch(`${window.origin}/eventtrigger`,{
   method: "POST",
   credentials: "include",
   body: JSON.stringify({filename,filesize}),
   cache: "no-cache",
   headers: new Headers({"content-type": "application/json"})   
   })
   .then(function(response){
       if (response.status == 200) {
       return response.json();
       }     
   })
   .then(function(data) {
       console.log(data);
       console.log(data.valid_filesize[0].status); 
       console.log(data.valid_extension[0].status); 
       if (data.valid_extension[0].status == 'False') {
           for (i=0; i < data.valid_extension[0].extensions.length-2;i++){
               x += "<." + data.valid_extension[0].extensions[i] + ">, ";
               }; 
           x += "<." + data.valid_extension[0].extensions[data.valid_extension[0].extensions.length-2] + "> and <." + data.valid_extension[0].extensions[data.valid_extension[0].extensions.length-1] + ">";
           $("#eventresponse").text(`Invalid file extension: only ${x} allowed.`);
       } else if (data.valid_filesize[0].status == 'False'){
           var filesize = data.valid_filesize[0].filesize/1024/1024
           $("#eventresponse").text(`Filesize exceeds the limit of <${filesize.toFixed(2)} MB>.`);
       } else {
       console.log("cleared");
       $("#eventresponse").text(``);
       }
   })
   .catch((error) => console.log(error))    
});

