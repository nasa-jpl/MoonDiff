const comparerHelp = document.getElementById("comparer-help");
const tourlink = document.getElementById("tour-link");

comparerHelp.style.display = "block";

const tour = new Shepherd.Tour({
  useModalOverlay: true,
  defaultStepOptions: {
    classes: "shadow-md bg-purple-dark",
    scrollTo: true,
  },
});

const tourButtons = [
  {
    text: "Next",
    action: tour.next,
  },
];

tour.addStep({
  id: "comparer",
  text: `<p>Explore this map to detect changes. If you notice a difference between the images:
            <ul>
            <li>Click once on the map to begin drawing a polygon around the difference.</li>
            <li>Double-click, or click back on the first point, to finish drawing, or use the Esc key to cancel.</li>
            <li>A popup will ask you a couple of questions to finish submitting your detection.</li>
            </ul>
        </p>
        <p>Map navigation works like most other web maps:
        <ul>
            <li>To pan the map, either click and drag or use the arrow keys on your keyboard</li>
            <li>To zoom the map, use your mousewheel or the + - keys on your keyboard.</li>
        </ul>
        </p>
        `,
  attachTo: {
    element: "#map-area",
  },
  buttons: [
    {
      text: "Next",
      action: tour.next,
    },
  ],
});

tour.addStep({
  id: "comparer-mode",
  text: `<p>Moondiff has two ways of comparing images: side-by-side, and blink / fade mode. You can experiment with 
    both, or stick with your favorite.</p>
     <p>Once you've viewed the entire overlap area of the image pair at high resolution and have reported any 
     differences, click <b>pair done</b> and you will be randomly assigned a new image pair to examine. If you'd like to
     skip this image pair and come back to it at some point in the future, click <b>skip pair</b>.</p>
    `,
  attachTo: {
    element: "#page-tools",
    on: "bottom",
  },
  buttons: tourButtons,
});

tour.addStep({
  id: "image-controls",
  text:
    "The image controls allow you to adjust the display of the images individually. In blink / fade mode, a white" +
    "arrow next to the image controls informs you which image is currently displayed.",
  attachTo: {
    element: "#left-image-controls",
    on: "top",
  },
  buttons: tourButtons,
});

tour.addStep({
  id: "comments",
  text: "Record any general observations about this image pair here.",
  attachTo: {
    element: "#comments",
    on: "left",
  },
  buttons: tourButtons,
});

tour.addStep({
  id: "detections",
  text: "This tool can be used to manage detections you have reported on this image pair.",
  attachTo: {
    element: "#detections",
    on: "left",
  },
  buttons: tourButtons,
});

tourlink.addEventListener("click", (evt) => {
  tour.start();
  evt.preventDefault();
});
