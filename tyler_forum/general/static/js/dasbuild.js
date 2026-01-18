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