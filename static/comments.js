const comments = document.getElementById("comments");
const commentsTitle = document.getElementById("comments-title");
const commentsForm = document.querySelector("#comments form");
const _csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
commentsTitle.addEventListener('click', (evt) => {
    comments.classList.toggle('collapsed');
});
commentsForm.addEventListener('submit', () => {
    const commentData = new FormData(commentsForm);
    console.log('posting comment');
    fetch('/api/comments/', {
        method: 'POST',
        credentials: 'same-origin',
        body: commentData,
        headers: {'x-csrftoken': _csrfToken}
    });
});