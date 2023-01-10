const nextButton = document.querySelector('#skip-button');
const visitPk = document.querySelector('#visit_id').value;
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const pairId = document.querySelector('[name=pair_id]').value;
const comparerModeChooser = document.querySelector('#comparer-mode').value;
// const csrfToken = getCookie('csrftoken');
nextButton.addEventListener('click', () => {
    window.location.href = data.nextUrl;
});

const doneButton = document.querySelector('#done-button');
const visitData = new FormData();
visitData.append('csrfmiddlewaretoken', csrfToken);
visitData.append('pair', pairId);

doneButton.addEventListener('click', () => {
    visitData.append('finished', true);
    fetch(`/api/visits/${visitPk}/`, {
            method: 'PUT',
            credentials: 'same-origin',
            body: visitData,
            headers: {'x-csrftoken': csrfToken}
        }
    );
    window.location.href = `${data.nextUrl}?comparerMode=${comparerModeChooser.value}`;
});

nextButton.addEventListener('click', () => {
    visitData.append('finished', false);
    fetch(`/api/visits/${visitPk}/`, {
            method: 'PUT',
            credentials: 'same-origin',
            body: visitData,
            headers: {'x-csrftoken': csrfToken}
        }
    );
    window.location.href = `${data.nextUrl}?comparerMode=${comparerModeChooser.value}`;
});