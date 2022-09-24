// // function addFields(){
// //     // Generate a dynamic number of inputs
// //     var number = document.getElementById("jumlah-tugas").oninput;
// //     // Get the element where the inputs will be added to
// //     var container = document.getElementById("container-divisi");
// //     // Remove every children it had before
// //     while (container.hasChildNodes()) {
// //         container.removeChild(container.lastChild);
// //     }
// //     for (i=0;i<number;i++){
// //         // Append a node with a random text
// //         container.appendChild(document.createTextNode("Member " + (i+1)));
// //         // Create an <input> element, set its type and name attributes
// //         var input = document.createElement("input");
// //         input.type = "text";
// //         input.name = "member" + i;
// //         container.appendChild(input);
// //         // Append a line break 
// //         container.appendChild(document.createElement("br"));
// //     }
// // }

// function addFields(x) {
//     var maxField = 100; //Input fields increment limitation
//     var addButton = $('.add_button'); //Add button selector
//     var wrapper = $('.field_wrapper_'+x); //Input field wrapper
//     var fieldHTML = '<div><input type="text" name="field_name[]" value=""/><a href="javascript:void(0);" class="remove_button"><img src="{% static 'event_kepanitiaan/img/remove - icon.png' %}" width="18" height="18"/></a></div>'; //New input field html 
//     var x = 1; //Initial field counter is 1

//     //Once add button is clicked
//     $(addButton).click(function () {
//         //Check maximum number of input fields
//         if (x < maxField) {
//             x++; //Increment field counter
//             $(wrapper).append(fieldHTML); //Add field html
//         }
//     });

//     //Once remove button is clicked
//     $(wrapper).on('click', '.remove_button', function (e) {
//         e.preventDefault();
//         $(this).parent('div').remove(); //Remove field html
//         x--; //Decrement field counter
//     });
// }
