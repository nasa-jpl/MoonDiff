const detections = document.getElementById("detections");
const detectionsTitle = document.getElementById("detections-title");
const detectionDelButtons = document.querySelectorAll('.detection-del-button')
detectionsTitle.addEventListener('click', () => {
    detections.classList.toggle('collapsed');
});

for (delButton of detectionDelButtons){
    delButton.addEventListener('click',(evt)=>{
    const detectionUrl = evt.target.dataset.detectionUrl;
    fetch(detectionUrl,{
            method: 'DELETE',
            credentials: 'same-origin',
            headers: {'x-csrftoken': _csrfToken}
        }
    ).then(
        (response) => {
            if (response.ok) {
                evt.target.parentElement.remove()
                window.location.reload()
            } else {
                alert('There was a problem deleting your change detection.');
            }
        }
    );
})
}
