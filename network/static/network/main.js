document.addEventListener('DOMContentLoaded', ()=>{
    document.querySelectorAll('.edit-btn').forEach(button =>{
        button.onclick = function(e){
            // grab text, change to text field, enter old text, get new, send, update

            if(button.innerHTML == 'Edit'){
                button.innerHTML = 'Save';
                let parent = e.target.parentNode;

                let contentBox = parent.querySelector('.content');
                contentBox.hidden = true;

                let textArea = parent.querySelector('.edit-area');
                textArea.innerHTML = contentBox.innerHTML;
                textArea.hidden = false;
            }
            else if(button.innerHTML == 'Save'){
                button.innerHTML = 'Edit'

                let parent = e.target.parentNode;
                let postID = parent.dataset.postid;

                let contentBox = parent.querySelector('.content');
                contentBox.hidden = false;

                let textArea = parent.querySelector('.edit-area');
                contentBox.innerHTML = textArea.value;
                textArea.hidden = true;

                // prepare data
                let data = {'postID':postID, 'text': textArea.value}

                // send update
                fetch('/edit', {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest', 
                        'X-Csrftoken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify(data)
                }).then(response=>{
                    return response.json()
                }).then(data=>{
                    // log response
                    console.log(data)
                })
            }
        }
    })
    document.querySelectorAll('.like').forEach(form =>{
        form.addEventListener('submit', e=> {
            // ignore default behavior
            e.preventDefault()
            
            // get parent element and the post ID
            let parent = e.target.parentNode;
            let postID = parent.dataset.postid;

            // prepare data to be sent
            let data = {'postID': postID}

            // fetch call
            fetch('/likes', {
                method:'POST',
                credentials: 'same-origin',
                headers:{
                    "X-Requested-With": "XMLHttpRequest",
                    "X-Csrftoken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(data)
            }).then(response=>{
                return response.json()
            }).then(data=>{
                // update the count on the button
                count = data['likes']
                likeButton = parent.querySelector('.like-btn')
                likeButton.innerHTML = `Likes: ${count}`
            })
        })
    })
});
