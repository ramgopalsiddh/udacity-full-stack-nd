// operation for lists
function createList() {
    // create new lists oprtation
    document.getElementById('listform').onsubmit = function (e) {
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
            .then(function (res) {
                // console.log("in the first then", res.json());
                return res.json();
            })
            .then(function (res) {
                // console.log("in the second then", res.json());
                console.log("Success", res);
                window.location.href = '';


                document.getElementById('error').classname = 'hidden';
            })
            .catch(function (error) {
                console.log("error occured in calling create", error);
                document.getElementById('error').classname = error;
            })
    }

}

function deleteList() {

// delete option for lists
const listdeleteBtns = document.querySelectorAll('.delete-list');
for (let i = 0; i < listdeleteBtns.length; i++) {
    const btn = listdeleteBtns[i];
    btn.onclick = function (e) {
        const listId = btn.getAttribute('data-listId');
        fetch('/lists/' + listId, {
            method: 'DELETE'
        })
            .then(function (response) {
                console.log("Success", response);
                window.location.href = '';
            })
            .catch(function () {
                console.log("Error", response);
            })
    }
}

    
}
