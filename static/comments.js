const comments = document.getElementById("comments");
const commentsTitle = document.getElementById("comments-title");
const commentsForm = document.querySelector("#comments form");
const _csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
const comments_url = document.currentScript.dataset.commentsUrl;
commentsTitle.addEventListener("click", (evt) => {
  comments.classList.toggle("collapsed");
});
commentsForm.addEventListener("submit", (evt) => {
  const commentData = new FormData(commentsForm);
  console.log("posting comment");
  fetch(comments_url, {
    method: "POST",
    credentials: "same-origin",
    body: commentData,
    headers: { "x-csrftoken": _csrfToken },
  }).then(resp => {
    if (resp.ok){
      alert("Comment successfully submitted, thanks!");
      commentsForm.querySelector("textarea").value = "";
      comments.classList.toggle("collapsed");
    }
  });
  evt.preventDefault();
});
