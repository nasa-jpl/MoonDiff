const tour = new Shepherd.Tour({
    useModalOverlay: true,
    defaultStepOptions: {
        classes: 'shadow-md bg-purple-dark',
        scrollTo: true
    }
});

tour.addStep({
    id: 'comparer-mode',
    text: 'Moondiff has two ways of comparing images: side-by-side, and blink / fade mode. You can experiment with both,' +
        ' or stick with your favorite.',
    attachTo: {
        element: '#comparer-mode',
        on: 'bottom'
    },
    buttons: [
        {
            text: 'Next',
            action: tour.next
        }
    ]
});

tour.start();