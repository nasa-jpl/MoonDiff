for (const imgLbl of document.querySelectorAll('.image-id')){
    imgLbl.addEventListener('click',
        (evt)=>{
            MicroModal.show('pair-info-modal')
        }
    )
}