const examples = document.getElementById("examples");
const examplesTitle = document.getElementById("examples-title");
examplesTitle.addEventListener("click", () => {
  examples.classList.toggle("collapsed");
});

const exampleNotes = document.getElementById("example-notes");
const examplesNotesTitle = document.getElementById("example-notes-title");
examplesNotesTitle.addEventListener("click", () => {
  exampleNotes.classList.toggle("collapsed");
});