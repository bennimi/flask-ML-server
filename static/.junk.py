
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