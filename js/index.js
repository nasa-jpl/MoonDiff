import Map from "@arcgis/core/WebMap";
import MapView from "@arcgis/core/views/MapView";
import ImageryTileLayer from "@arcgis/core/layers/ImageryTileLayer";
import Draw from "@arcgis/core/views/draw/Draw"

// TODO sourcemap
// TODO link maps
// TODO drawing
// TODO drawing submission
// TODO next / prev buttons, viewed by user recording
// TODO offsets

// TODO find a better way than using window for making this function accessible from the django template
window.makeTileMap = (tile_url, container)=>{
    const webmap = new Map({});
    const locog = new ImageryTileLayer({
        url: tile_url,
        // url: 'https://oin-hotosm.s3.amazonaws.com/56f9b5a963ebf4bc00074e70/0/56f9c2d42b67227a79b4faec.tif'
    })
    webmap.layers.add(locog);
    const view = new MapView({
        container: container,
        map: webmap
    })
    return view
}