// data from the script tag data properties
const data = document.currentScript.dataset;

const setup = (comparerMode) => {
    require(["esri/Map",
        "esri/views/MapView",
        "esri/layers/ImageryTileLayer",
        "esri/views/draw/Draw",
        "esri/layers/GraphicsLayer",
        "esri/Graphic",
        "esri/widgets/Sketch",
        "esri/layers/support/TileInfo",
        "https://unpkg.com/micromodal/dist/micromodal.min.js"
    ], function (
        Map, MapView, ImageryTileLayer, Draw, GraphicsLayer, Graphic, Sketch, TileInfo, MicroModal) {
        MicroModal.init();

        const makeTileMap = (tile_url, container) => {
            const webmap = new Map({});
            const tileLayer = new ImageryTileLayer({
                url: tile_url,
            });
            webmap.layers.add(tileLayer);
            return new MapView({
                container: container,
                map: webmap,
                constraints: {
                    snapToZoom: false,
                    maxScale: 0,
                    lods: TileInfo.create().lods
                }
            });
        };

        function createPoint(lat, lon) {
            const point = {
                type: "point",
                longitude: lon,
                latitude: lat
            };

            // Create a symbol for drawing the point
            const markerSymbol = {
                type: "simple-marker",
                style: "cross"
            };

            // Create a graphic and add the geometry and symbol to it
            return new Graphic({
                geometry: point,
                symbol: markerSymbol
            });
        }

        const mainview = makeTileMap(data.oldImageUrl, 'left_mapview_container');
        const oldImageLayer = mainview.map.layers.items[0];
        registerImageControlsOnLayer(oldImageLayer, 'left');
        mainview.crosshair = createPoint(0, 0);
        mainview.graphics.add(mainview.crosshair);
        const annotationLayer = new GraphicsLayer();
        const annotationLayerCopy = new GraphicsLayer();
        mainview.map.layers.add(annotationLayer);


        const addPolylinesToLayer = (layer, polylines) => {
            const polyLinesArray = polylines.map((polyline) => {
                    const polylineGraphic = new Graphic({
                            geometry: {
                                type: 'polygon',
                                rings: polyline
                            },
                            symbol: {
                                type: "simple-line"
                            }
                        }
                    );
                    layer.add(polylineGraphic);
                    return polylineGraphic;
                }
            );
            return polyLinesArray;
        };
        const polylines = JSON.parse(document.getElementById("polylines").textContent);

        if (comparerMode === 'sideBySide') {
            const rightview = makeTileMap(data.newImageUrl, 'right_mapview_container');
            registerImageControlsOnLayer(rightview.map.layers.items[0], 'right');
            rightview.crosshair = createPoint(0, 0);
            rightview.graphics.add(rightview.crosshair);
            const views = [mainview, rightview];
            let active = mainview;


            rightview.map.layers.add(annotationLayerCopy);
            let polylineGraphics = addPolylinesToLayer(annotationLayerCopy, polylines);
            addPolylinesToLayer(annotationLayer, polylines);
            // TODO move these functions into libraries


            const sync = (source) => {
                // Sets the center and zoom of all views to the center and zoom of source
                if (!active || !active.viewpoint || active !== source) {
                    return;
                }

                for (const view of views) {
                    if (view !== source) {
                        view.viewpoint = source.viewpoint;
                    }
                }
            };

            const syncPointer = (evt) => {
                // Copies the crosshair for drawing polygons to all views
                for (const view of views) {
                    const cursor_coord = view.toMap({x: evt.x, y: evt.y});
                    view.crosshair.geometry = {
                        type: 'point',
                        x: cursor_coord.longitude,
                        y: cursor_coord.latitude
                    };
                }
            };

            for (const view of views) {
                view.when(() => {
                        view.goTo({target: polylineGraphics}, {animate: false});
                        // TODO next line doesn't seem to work, maybe firing too son
                        view.zoom = view.zoom - 2;
                    }
                );
                view.watch(["interacting", "animation"], () => {
                    active = view;
                });

                view.watch("viewpoint", () => sync(view));
                view.on("pointer-move", syncPointer);
                view.watch('updating', (evt) => {
                    if (evt === true) {
                        document.querySelector('.loading').style.display = 'inline';
                    } else {
                        document.querySelector('.loading').style.display = 'none';
                    }
                });
            }
        } else {
            // assume blink mode
            mapArea = document.querySelector("#map-area");
            mapArea.style.gridTemplateColumns = "1fr 0";
            // workaround for "stars shining through" issue https://github.jpl.nasa.gov/MoonDiff/MoonDiff/issues/37
            mapArea.style.background = "black";
            const newImageLayer = new ImageryTileLayer({
                url: data.newImageUrl,
            });
            registerImageControlsOnLayer(newImageLayer, 'right');
            registerImageControlsOnLayer(oldImageLayer, 'left');
            mainview.map.add(newImageLayer);
            mainview.map.layers.add(annotationLayer); // re-add the annotation layer because otherwise it's underneath
            let polylineGraphics = addPolylinesToLayer(annotationLayer, polylines);
            mainview.when(() => {
                    mainview.goTo({target: polylineGraphics}, {animate: false});
                    // TODO next line doesn't seem to work, maybe firing too soon
                    mainview.zoom = mainview.zoom - 2;
                }
            );
            const fader = document.querySelector('#fader');
            fader.addEventListener('input', e => {
                oldImageLayer.opacity = 1 - e.target.value;
                newImageLayer.opacity = e.target.value;
                document.querySelector(".active-image-indicator.left").style.opacity = 1 - e.target.value;
                document.querySelector(".active-image-indicator.right").style.opacity = e.target.value;
            });
            let blinkSpeed = 1;
            let blinkHandle = null;
            const blinkSpeedSlider = document.querySelector('#blink-speed-slider');
            const updateBlinkfade = () => {
                blinkSpeed = blinkSpeedSlider.value;
                clearInterval(blinkHandle);
                blinkHandle = setInterval(() => {
                    if (blinkToggle.checked) {
                        if (fader.value == 1) {
                            fader.value = 0;
                        } else if (fader.value == 0) {
                            fader.value = 1;
                        } else {
                            fader.value = 0;
                        }
                        fader.dispatchEvent(new Event('input'));
                    }
                }, blinkSpeed * 1000);
            };
            blinkSpeedSlider.addEventListener('input', updateBlinkfade);
            const blinkToggle = document.querySelector('#blink-toggle');
            blinkToggle.addEventListener('input', updateBlinkfade);
            updateBlinkfade();
        }


        const submitAnnotationModal = async () => {
            return new Promise((resolve, reject) => {
                    MicroModal.show('annotation-notes-modal');
                    document.querySelector('#annotation-notes-submit').addEventListener(
                        "click", () => {
                            MicroModal.close('annotation-notes-modal');
                            resolve();
                        });
                    document.querySelector('#annotation-notes-close').addEventListener(
                        "click", () => {
                            reject();
                        }
                    );
                }
            );
        };


        const sketch = new Sketch({
            layer: annotationLayer,
            view: mainview,
            availableCreateTools: ["polygon"]
        });
        sketch.create("polygon");
        sketch.visible = false;
        annotationLayer.graphics.on('after-add', async (evt) => {
            const temp_poly = evt.item;
            const wkt_srid = evt.item.geometry.spatialReference.wkid;
            const wkt_points = evt.item.geometry.rings[0].map(pt => `${pt[0]} ${pt[1]}`).toString();
            const wkt_geometry = `SRID=${wkt_srid};POLYGON ((${wkt_points}))`;
            // only expected to work if we're in sideBySide mode
            let temp_poly_clone;
            try {
                temp_poly_clone = evt.item.clone();
                annotationLayerCopy.graphics.add(temp_poly_clone);
            } catch (e) {
            }
            await submitAnnotationModal().then(() => {
                    const annotationData = new FormData(document.querySelector("#annotation-notes-form"));
                    annotationData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
                    annotationData.append('shape', wkt_geometry);
                    fetch(data.annotationPostUrl, {
                        method: 'POST',
                        credentials: 'same-origin',
                        body: annotationData,
                        headers: {'x-csrftoken': csrfToken}
                    }).then(
                        (response) => {
                            if (response.ok) {
                                document.querySelector('.detections ul').textContent = 'Refresh the page to view new change detection reports.'
                                alert('Your change detection was successfully stored in the database.');
                            } else {
                                alert('There was a problem submitting your change detection.');
                            }
                        }
                    );
                }, () => {
                    temp_poly.layer.remove(temp_poly);
                    try {
                        temp_poly_clone.layer.remove(temp_poly_clone);
                    } catch (e) {
                    }
                }
            ); //TODO handle errors

        });
        mainview.ui.add(sketch, "top-right");
    });
};
// Get comparerMode from url param
const urlParams = new URLSearchParams(window.location.search);
let comparerMode = urlParams.get('comparerMode') || 'blinkFade';

// Set the dropdown box to the comparerMode of the url parameter & show blinkFade controls if we are in that mode
const comparerOptions = document.querySelector("#comparer-mode");
comparerOptions.value = comparerMode;
if (comparerMode === 'blinkFade') {
    document.querySelectorAll(".blinkfade.controls").forEach(el => {
        el.style.display = 'block';
    });
}

// If the dropdown changes, redirect the page to the right comparer
comparerOptions.addEventListener('change', (evt) => {
    urlParams.set('comparerMode', evt.target.value);
    window.location.search = urlParams.toString();
});
setup(comparerMode);