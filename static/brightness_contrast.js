var updateRenderer = (layer, evt)=>{
    let newRend = layer.renderer.clone()
    if (evt.target.name == "gamma-slider"){
        newRend.useGamma = true
        newRend.gamma = evt.target.value
    }
    else if (evt.target.name == "invert-toggle"){
        if (evt.target.checked){
            newRend.colorRamp = {
                type: "algorithmic",
                toColor: [0, 0, 0, 1],
                fromColor: [255, 255, 255, 1]
            }
        } else {
            newRend.colorRamp = {
                type: "algorithmic",
                fromColor: [0, 0, 0, 1],
                toColor: [255, 255, 255, 1]
            }
        }
    }
    else if (evt.target.name == "autostretch-toggle"){
        newRend.stretchType='min-max'
        newRend.dynamicRangeAdjustment = !newRend.dynamicRangeAdjustment
    }
    else if (evt.target.name == "reset"){
        evt.target.parentElement.querySelectorAll('input[type=checkbox]').forEach(
            (el)=>{
                el.checked = false;
                el.dispatchEvent(new Event('change'));
            }
        )
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
    document.querySelectorAll(`button.${side}`).forEach((el)=> {
        el.addEventListener('click', (evt) => {
            updateRenderer(layer, evt)
        })
    })
}