var updateRenderer = (layer, evt)=>{
    let newRend = layer.renderer.clone()
    if (evt.target.id == "gamma-slider"){
        newRend.useGamma = true
        newRend.gamma = document.getElementById("gamma-slider").value
    }
    if (evt.target.id == "invert-toggle"){
        if (!layer.renderer.colorRamp){
        //    No color ramp yet. We'll have to set one up before we can invert colors.
            layer.renderer.colorRamp = {
                    type: "algorithmic",
                    fromColor: [0, 0, 0, 1],
                    toColor: [255, 255, 255, 1]
            }
            newRend.colorRamp = layer.renderer.colorRamp
        }
        newRend.colorRamp.fromColor = layer.renderer.colorRamp.toColor
        newRend.colorRamp.toColor = layer.renderer.colorRamp.fromColor
    }
    if (evt.target.id == "autostretch-toggle"){
        newRend.dynamicRangeAdjustment = !newRend.dynamicRangeAdjustment
    }
    layer.renderer = newRend
    layer.refresh()
}

var registerImageControlsOnLayer = (layer, side) => {
    document.querySelectorAll(`.image-controls input.${side}`).forEach((el)=>{
        el.addEventListener('change',(evt)=>{
            updateRenderer(layer, evt)
        })
    })
}