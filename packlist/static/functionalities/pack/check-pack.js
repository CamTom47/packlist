    
    const $essentialModal = $('#essentialModal')
    const $body = $('body')

    let $modals = $('.modal')
    let modalIds = [];

    let $previousModal
    let $currentModal
    let $nextModal
    let currentIdx


    function getModalIds (modals){
        for(let modal of modals){
            modalIds.push(modal.id)
        }
    }

    function getCurrentModal(){
        console.log(currentIdx)
        if (currentIdx === undefined){
            currentIdx = 0
            $currentModal = $(`#${modalIds[currentIdx]}`)
            return $currentModal
        }
        $currentModal = $(`#${modalIds[currentIdx]}`)
        return $currentModal
    }
    
    function getCurrentIdx(){
        currentIdx = modalIds.indexOf($currentModal.attr('id'))
        return currentIdx
    }
    
    function getNextModal(){
        $nextModal = $(`#${modalIds[currentIdx + 1]}`)
        return $nextModal
    }
    
    function getPreviousModal(){
        $previousModal = $(`#${modalIds[currentIdx -1]}`)
        return $previousModal
    }
    
    $("body .next-button").on('click', ()=>{
        toggleNextModalUI()
        currentIdx++;
        getCurrentModal()
        getNextModal()
        getPreviousModal()

    })

    $("body .previous-button").on('click', ()=>{
        togglePreviousModalUI()
        currentIdx--;
        getCurrentModal()
        getNextModal()
        getPreviousModal()
    })


    function toggleNextModalUI(){
        if (currentIdx < modalIds.length){
                $currentModal.toggleClass('show')
                $currentModal.toggleClass('hide')
                $nextModal.toggleClass('hide')
                $nextModal.modal('show')
            }}


    function togglePreviousModalUI(){
        if (currentIdx < modalIds.length){
            console.log($currentModal)
            $currentModal.modal('hide')

            console.log($previousModal)
            $previousModal.toggleClass('show')
        }}

        

        $('document').ready(function(){
            getModalIds($modals)
            $currentModal = getCurrentModal()
            currentIdx = getCurrentIdx()
            $nextModal = getNextModal()
            $currentModal.modal('show')
            
        })