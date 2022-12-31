
// data from the script tag data properties
const data = document.currentScript.dataset

const setup = (comparerMode)=>{
    require(["esri/Map",
        "esri/views/MapView",
        "esri/layers/ImageryTileLayer",
        "esri/views/draw/Draw",
        "esri/layers/GraphicsLayer",
        "esri/Graphic",
        "esri/widgets/Sketch",
        "https://unpkg.com/micromodal/dist/micromodal.min.js"
    ], function (
        Map, MapView, ImageryTileLayer, Draw, GraphicsLayer, Graphic, Sketch, MicroModal){
        MicroModal.init()

        const nextButton = document.querySelector('#skip-button')
        nextButton.addEventListener('click',()=>{ window.location.href = data.nextUrl })

        const makeTileMap = (tile_url, container)=>{
            const webmap = new Map({});
            const tileLayer = new ImageryTileLayer({
                url: tile_url,
            })
            webmap.layers.add(tileLayer);
            return new MapView({
                container: container,
                map: webmap,
                constraints: {
                    snapToZoom: false
                }
            })
        }

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

        const mainview = makeTileMap(data.oldImageUrl, 'left_mapview_container')
        const oldImageLayer = mainview.map.layers.items[0]
        mainview.crosshair = createPoint(0,0)
        mainview.graphics.add(mainview.crosshair)
        const annotationLayer = new GraphicsLayer()
        const annotationLayerCopy = new GraphicsLayer()
        mainview.map.layers.add(annotationLayer)



        const addPolylinesToLayer = (layer, polylines) => {
            for (const polyline of polylines){
                layer.add(
                    new Graphic({
                            geometry: {
                                type: 'polygon',
                                rings: polyline
                            },
                            symbol: {
                                type: "simple-line"
                            }
                        }
                    )
                )
            }
        }
        const polylines = JSON.parse(document.getElementById("polylines").textContent)
        addPolylinesToLayer(annotationLayer, polylines)

        if (comparerMode === 'sideBySide'){
            const rightview = makeTileMap(data.newImageUrl, 'right_mapview_container')
            rightview.crosshair = createPoint(0,0)
            rightview.graphics.add(rightview.crosshair)
            const views = [mainview, rightview]
            let active = mainview


            rightview.map.layers.add(annotationLayerCopy)
            addPolylinesToLayer(annotationLayerCopy, polylines)

            // TODO move these functions into libraries


            const sync = (source) => {
                // Sets the center and zoom of all views to the center and zoom of source
                if (!active || !active.viewpoint || active !== source) {
                    return
                }

                for (const view of views) {
                    if (view !== source) {
                        view.viewpoint = source.viewpoint
                    }
                }
            }

            const syncPointer = (evt) => {
                // Sets the center and zoom of all views to the center and zoom of source
                for (const view of views) {
                    const cursor_coord = view.toMap({x:evt.x, y:evt.y})
                    view.crosshair.geometry= {
                        type: 'point',
                        x: cursor_coord.longitude,
                        y: cursor_coord.latitude
                    }
                }
            }

            for (const view of views) {
                view.watch(["interacting", "animation"], () => {
                    active = view
                })

                view.watch("viewpoint", () => sync(view))
                view.on("pointer-move", syncPointer)
                view.watch('updating', (evt) => {
                    if (evt === true){
                        document.querySelector('.loading').style.display='inline'
                    } else {
                        document.querySelector('.loading').style.display='none'
                    }
                })
            }
        }
        else {
            // assume blink mode
            document.querySelector("#map-area").style.gridTemplateColumns = "1fr 0";
            const newImageLayer = new ImageryTileLayer({
                url: data.newImageUrl,
            })
            mainview.map.add(newImageLayer)
            mainview.map.layers.add(annotationLayer) // re-add the annotation layer because otherwise it's underneath
            const fader = document.querySelector('#fader')
            fader.addEventListener('input', e=>{
                oldImageLayer.opacity = e.target.value;
                newImageLayer.opacity = 1-e.target.value;
            })
            let blinkSpeed = 1
            let blinkHandle = null
            const blinkSpeedSlider = document.querySelector('#blink-speed-slider')
            const updateBlinkfade = ()=>{
                blinkSpeed = blinkSpeedSlider.value
                clearInterval(blinkHandle)
                blinkHandle = setInterval(() => {
                    if (blinkToggle.checked) {
                        if (fader.value == 1) {
                            fader.value = 0
                        } else if (fader.value == 0) {
                            fader.value = 1
                        } else {
                            fader.value = 0
                        }
                        fader.dispatchEvent(new Event('input'))
                    }
                }, blinkSpeed * 1000)
            }
            blinkSpeedSlider.addEventListener('input', updateBlinkfade)
            const blinkToggle = document.querySelector('#blink-toggle')
            blinkToggle.addEventListener('input', updateBlinkfade)
            updateBlinkfade()
        }


        const submitAnnotationModal = async() => {
            return new Promise((resolve) => {
                    MicroModal.show('annotation-notes-modal')
                    document.querySelector('#annotation-notes-submit').addEventListener(
                        "click", ()=>{
                            MicroModal.close('annotation-notes-modal')
                            resolve()
                        })
                }
            )
        }




        const sketch = new Sketch({
            layer: annotationLayer,
            view: mainview,
            availableCreateTools: ["polygon"]
        });
        sketch.create("polygon")
        sketch.visible = false
        annotationLayer.graphics.on('after-add', async (evt) => {
            const wkt_srid = evt.item.geometry.spatialReference.wkid
            const wkt_points = evt.item.geometry.rings[0].map(pt=>`${pt[0]} ${pt[1]}`).toString()
            const wkt_geometry = `SRID=${wkt_srid};POLYGON ((${wkt_points}))`
            // only expected to work if we're in sideBySide mode
            try{annotationLayerCopy.graphics.add(evt.item.clone())} catch(e){}
            await submitAnnotationModal().then(()=>{
                    const annotationData = new FormData(document.querySelector("#annotation-notes-form"));
                    annotationData.append('csrfmiddlewaretoken',document.querySelector('[name=csrfmiddlewaretoken]').value)
                    annotationData.append('shape',wkt_geometry)
                    fetch(data.annotationPostUrl, {
                        method: 'POST',
                        credentials: 'same-origin',
                        body: annotationData
                    })
                },  ()=>{
                    console.log("not submitted")
                }


            ) //TODO handle errors

        })
        mainview.ui.add(sketch, "top-right")
    })
}
// Get comparerMode from url param
const urlParams = new URLSearchParams(window.location.search)
let comparerMode = urlParams.get('comparerMode') || 'blinkFade'

// Set the dropdown box to the comparerMode of the url parameter & show blinkFade controls if we are in that mode
const comparerOptions = document.querySelector("#comparer-mode")
comparerOptions.value = comparerMode
if (comparerMode === 'blinkFade'){
    document.querySelectorAll(".blinkfade.controls").forEach(el=>{el.style.display='block'})
}

// If the dropdown changes, redirect the page to the right comparer
comparerOptions.addEventListener('change', (evt)=>{
    urlParams.set('comparerMode', evt.target.value)
    window.location.search = urlParams.toString()
})
setup(comparerMode)