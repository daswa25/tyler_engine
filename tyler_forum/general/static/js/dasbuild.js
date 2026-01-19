class FormsBuild{
    constructor(formID,listForm,edit){
        this.formID=formID;
        this.listForm=listForm;
        this.edit=edit;
    }
    generate() {
    // CUSTOM FORM
    try {
            if (!Array.isArray(this.listForm)) {
                throw new Error("listForm must be an array of field objects.");
            }

            
            let formTemplate = `<form id="${this.formID}">`;
            var edit=this.edit;
            var edited=""
            if(edit==1){
                 edited=`readonly="true" title="You can't edit "`;
            }else{
                edited=" title='Now you can edit'";
            }
            
         
            this.listForm.forEach(field => {
                formTemplate += `<div class="form-group">`;
                
               
                if (field.label) {
                    formTemplate += `<label for="${field.id}">${field.label}</label>`;
                }
                switch (field.type) {
                    case 'select':
                        formTemplate += `<select id="${field.id}" name="${field.name}" class="form-control">`;
                        field.options.forEach(opt => {
                            formTemplate += `<option value="${opt.value}">${opt.text}</option>`;
                        });
                        formTemplate += `</select>`;
                        break;
                    
                    case 'textarea':
                        formTemplate += `<textarea id="${field.id}" name="${field.name}" placeholder="${field.placeholder || ''}"></textarea>`;
                        break;

                    default:
                        formTemplate += `<input type="${field.type}" id="${field.id}" value="${field.value}" name="${field.name}" placeholder="${field.placeholder || ''}" class="form-control" ${edited}>`;
                }

                formTemplate += `</div>`;
            });

            // Close the form and add a submit button
            formTemplate += `<p class='mt-4 alert alert-info'>Update your details</p>`;
            formTemplate += `</form> <div id='output-bio'></div>`;

            return formTemplate;

        } catch (error) {
            console.error("Form Generation Error:", error);
            return null;
        }
    }


}
function preview(width,height,radius){
    var src= $("#preview").attr('src');
    var img_name=$("#raw_img").text("Current Profile Picture");
    console.log(src);
    $("#max-width").html(`<img  class='d-flex ms-auto me-auto mt-3' src='${src}' style='width:${width}px;height:${height}px;border-radius:${radius}%'>`);
}
var cropper;
function uploadImg(){
    alert("event is triggered");
    var imageFile=$('#hidden_img')[0];
    console.log(imageFile.files);
    if(imageFile.files && imageFile.files[0]){
        var files = imageFile.files[0];
       
        var fileRead= new FileReader()
       
        // PRE-VIEW
        fileRead.onload=(e)=>{
            var base64= e.target.result;
            //CONTAINER FOR CROP SHOW
            $('#custom-crop-area').show();
            var image_crop=$("#target-img");
            image_crop.attr('src',e.target.result)
            // INITIAL CSS
            $("#crop-box").css({"top":0,"left":0});
            cropX=0;
            cropY=0;
            var imageUpload= new Image();
            imageUpload.src= e.target.result;
            imageUpload.onload=function(){
                naturalWidth=this.width;
                naturalHeight=this.height;
            };
            
            console.log("Image Uploaded"+base64);
            $("#max-width").html(`<div class="spinner-border d-flex ms-auto me-auto mb-3" role="status" style="color:#252653;"><span class="visually-hidden">Loading...</span></div>`)
            setTimeout(()=>{
                preview(base64,350,276,20);
            },2000);
            
            
        }
        
            console.log(fileRead.readAsDataURL(files));
            var form_data= new FormData();
        // preview(files.name,350,276,20);
            form_data.append('image',files)


    }

}
//DRAGGABLE CROP 
$(document).ready(function(){
    var isDragging= false;
    var startX,startY,initialBoxX,initialBoxY;
    $("#target-img").show();
    // DRAG STARTS
    $("#crop-box").mousedown(function(e){
        isDragging=true;
        startX=e.clientX;
        startY=e.clientY;
        console.log(`x${startX}&Y${startY}`);
        //Getting the box position
        var pos= $(this).position();
        initialBoxX=pos.left;
        initialBoxY=pos.top;
        console.log(`left${initialBoxX} and top ${initialBoxY}`);
        //STOPS THE UNWANTED BEHAVIOUR;
        e.preventDefault();
    });
//MAKE THE BOX MOVE
    $(document).mousemove(function(e){
        if(isDragging){
            var moveX,moveY,newLeft,newTop,imgWidth,imgHeight,boxSize;
            moveX=e.clientX-startX;
            moveY=e.clientY-startY;
            console.log(`move-x${moveX} move-y${moveY}`);
            newLeft=initialBoxX+moveX;
            newTop=initialBoxY+moveY;
            // BOUNDARY LIMIT 
            imgWidth=$('#target-img').width();
            imgHeight=$("#target-img").height();
            boxSize=200;
            if(newLeft<0) newLeft=0;
            if(newTop<0) newTop=0;
            if(newLeft+boxSize>imgWidth) newLeft=imgWidth-boxSize;
            if(newTop+boxSize>imgHeight) newTop=imgHeight-boxSize;
            $("#crop-box").css({top:newTop,left:newLeft});
            cropX=newLeft;
            cropY=newTop;
        }
        
         
    });
    //CROPPED
    $(document).mouseup(function() {
        isDragging = false;

    });
});
function cropIt(flag,id){
    if(flag==1){
    if(!naturalWidth) {
        alert("Image not fully loaded yet. Please wait a moment.");
        return;
    }
    console.log(cropX+"-"+cropY);
    var canvas = document.getElementById('hidden-canvas');
    var ctx=canvas.getContext('2d');
    var imgEle=document.getElementById('target-img');
    
    //SCALING
    var displayWidth=$('#target-img').width();
    var scaleRatio= naturalWidth/displayWidth;
    //SQUARE-CUT
    var boxSize = 200; 
    var realSize = Math.floor(boxSize * scaleRatio);
    console.log(realSize+"--real size");
    // POSITION OF THE IMAGE;
    var scaleX=Math.floor(cropX*scaleRatio);
    var scaleY=Math.floor(cropY*scaleRatio);
    //FIXED WIDTH AND HEIGHT;
    var scaleWidth=realSize;
    var scaleHeight=realSize;
    if(scaleX<0)scaleX=0;
    if(scaleY<0)scaleY=0;
    if(scaleX+scaleWidth > naturalWidth){scaleX=naturalWidth-scaleWidth;}
    if(scaleY+scaleHeight > naturalHeight){scaleY=naturalHeight-scaleHeight;}
    


    var final= 350;
    canvas.width=final;
    canvas.height=final;
    console.log(`Scale Ratio: ${scaleRatio}`);
    console.log(`Cutting: X=${scaleX}, Y=${scaleY}, W=${scaleWidth}, H=${scaleHeight}`);
    ctx.drawImage(imgEle,scaleX,scaleY,scaleWidth,scaleHeight,0,0,final,final);
    var previewUrl=canvas.toDataURL('image/jpeg');
    $("#target-img").hide();
    $('#profile-picture').attr('src',previewUrl);
    $('#profile-picture').attr('class','d-flex ms-auto me-auto');
    canvas.toBlob(function(blob){
        var formData= new FormData();
        formData.append('image',blob,'cropped_image.jpg');
        var token=$("input[name=csrfmiddlewaretoken]").val();
        formData.append('csrfmiddlewaretoken',token);
        formData.append('id',id);
        $('.btn-success').text('Save to Profile');
        $.ajax({
            url:'/api/upload_profilepic',
            method:'POST',
            data:formData,
            processData:false,
            contentType:false,
            success:function(response){
                if(response.message==true){
                  
                    window.location='/api/forum';
                      getProfilePic(id)
                }else{
                    alert("danger");
                }
            },
            error:function(){
            $('.btn-success').text('Save to Profile');
            }
        },'image/jpeg',0.9);
    });


    }
}
