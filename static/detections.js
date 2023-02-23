const detections = document.getElementById("detections");
const detectionsTitle = document.getElementById("detections-title");
const detectionDelButtons = document.querySelector('.detection-del-button')
detectionsTitle.addEventListener('click', (evt) => {
    detections.classList.toggle('collapsed');
});

detectionDelButtons.addEventListener('click',(evt)=>{
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
            } else {
                alert('There was a problem deleting your change detection.');
            }
        }
    );
})