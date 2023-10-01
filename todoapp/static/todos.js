function createTodo() {
  // create new todo
  document.getElementById('form').onsubmit = function(e) {
    var list_id = document.getElementById('form').getAttribute('data-activeListId');
    e.preventDefault();
    fetch('/todos/create', {
        method: 'POST',
        body: JSON.stringify({
            'list_id': list_id,
            'description': document.getElementById('description').value
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
}

function completeTodo() {
    // check box for todos
    const checkboxes = document.querySelectorAll('.check-completed');
    for (let i = 0; i < checkboxes.length; i++) {
        const checkbox = checkboxes[i];
        checkbox.onchange = function(e) {
            const newCompleted = e.target.checked;
            const todoId = checkbox.getAttribute('data-todoId');
            fetch('/todos/' + todoId + '/set-completed', {
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
}

function deleteTodo() {
  // delete for todo
     const deleteBtns = document.querySelectorAll('.delete-button');
     for (let i = 0; i < deleteBtns.length; i++) {
         const btn = deleteBtns[i];
         btn.onclick = function(e) {
            const todoId = btn.getAttribute('data-todoId');
            fetch('/todos/' + todoId, {
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
   
}
