
# check input size old 

if not type(request.get_json()) == None and \
request.get_json() <= app.config["ALLOWED_FILE_UPLOAD_SIZE"]:
    print("Uploaded file exceeds the size limit {} : {}".format(app.config["ALLOWED_FILE_UPLOAD_SIZE"],request.get_json()),flush=True)
    return render_template('file_predict.html',context=context)
else:
    app.config["ALLOWED_FILE_UPLOAD_CHECKER"] = True
    print(app.config["ALLOWED_FILE_UPLOAD_CHECKER"] ,flush=True)
    return render_template('file_predict.html',context=context)


# check input size old 
if not int(request.cookies.get('filesize')) <= app.config["ALLOWED_FILE_UPLOAD_SIZE"]:
     print("Uploaded file exceeds the size limit {} : {}".format(
       app.config["ALLOWED_FILE_UPLOAD_SIZE"],
       request.cookies.get('filesize')),flush=True)
     return redirect(request.url)
 
    
 # check input with async respone and returned newly returned page
 {% if filename == 'True'%}
       <input class="form-control" id="hidden-input" type="hidden"> 
 {%endif%}
 
 
 ######
 $("#submit").bind("click",function(){
    fetch(`${window.origin}/eventtrigger`,{
   method: "POST",
   credentials: "include",
   body: JSON.stringify("filesize"),
   cache: "no-cache",
   headers: new Headers({"content-type": "application/json"})
   })
    .then(function(response){
        return response.json();
    })
    .then(function(data){
    console.log(data.event_trigger);
    $("#response").html(data.event_trigger);
    }); 
});
 
 
 ######
 
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
           for (i=0; i < data.valid_extension[0].extensions.length-1;i++){
               x += "." + data.valid_extension[0].extensions[i] + ", ";
               }; 
           x += "." + data.valid_extension[0].extensions[data.valid_extension[0].extensions.length-1];
           $("#eventresponse").text(`Please input a file extension: ${x} allowed.`);
       } else if (data.valid_filesize[0].status == 'False'){
           var filesize = data.valid_filesize[0].filesize/1024/1024
           $("#eventresponse").text(`Filesize exceeds the limit of: ${filesize.toFixed(2)} MB.`);
       } else {
       console.log("cleared");
       }
   })
   .catch((error) => console.log(error))    
});
