
     // operation for lists

      // create new lists oprtation
/*
      document.getElementById('listform').onsubmit = function(e) {
        var list_id = document.getElementById('listform').getAttribute('data-activeListId');
        e.preventDefault();
        fetch('/lists/create', {
            method: 'POST',
            body: JSON.stringify({
                //'list_id': list_id,
                'name': document.getElementById('todolist-input').value
            }),
            headers: {
                'Content-type': 'application/json'
            }
        })
        .then(function(res) {
            // console.log("in the first then", res.json());
            return res.json();
        })
        .then(function(res) {
            // console.log("in the second then", res.json());
            console.log("Success", res);
            window.location.href = '';

            
            document.getElementById('error').classname='hidden';
        })
        .catch(function(error) {
            console.log("error occured in calling create", error);
            document.getElementById('error').classname = error;
        })
    }  
    
    
// checkbox for lists 

    const listcheckboxes = document.querySelectorAll('.check-completed');
    for (let i = 0; i < listcheckboxes.length; i++) {
        const checkbox = listcheckboxes[i];
        checkbox.onchange = function(e) {
            const newCompleted = e.target.checked;
            const todoId = checkbox.getAttribute('data-listId');
            fetch('/lists/' + listId + '/set-completed', {
                method: 'POST',
                body: JSON.stringify({
                    'completed': newCompleted
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(function(res){
                console.log("Success", res);
                window.location.href = '';
                document.getElementById('error').className = 'hidden';
            }) 
            .catch(function (error) {
                document.getElementById(error).className = '';
                console.log("error occured in setting complete", error);
            })
        }
    }

  // delete option for lists 

    const listdeleteBtns = document.querySelectorAll('.delete-button');
    for (let i = 0; i < listdeleteBtns.length; i++) {
        const btn = listdeleteBtns[i];
        btn.onclick = function(e) {
            const todoId = btn.getAttribute('data-listId');
            fetch('/lists/' + listId, {
                method: 'DELETE'
            })
            .then(function(response){
              console.log("Success", response);
              window.location.href = '';
            })
             .catch(function(){
              console.log("Error", response);
            })
        }
    }
*/
