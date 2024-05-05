const $itemSectionBtn = $('#item-section-button')
const $packSection = $('#pack-section')
const $packForm = $('#pack-form')
const $createPackBtn = $('#create-pack-button')

let categories = new Set()

async function getCategories()  {
    let resp = await axios.get(`/api/items`)
    let items = resp.data.items    

    for(let item of items) {
       categories.add(item.category)
    }

    return(resp.data.items)
}

$itemSectionBtn.on('click', async (e)=>  {
    e.preventDefault()
    let items = await Promise.resolve(getCategories())

    $packForm.after('<div id="item-section" class="d-inline w-75"></div>')
    
    $("#item-section").append(`<div id="category-section" class="d-inline w-100"></div>`)
    
    for(let category of categories){
        $('#category-section').append(`

        <h3 class="ms-3 text-bg-dark text-light">
                        ${category}
                    </h3>
                    <hr>
                    <ul id="${category}">
                        <div id="${category}-row" class="row bg-light">
                        </div>
                        </ul>`)
                        

        for(let item of items){
            
            if(item.category === category){
                $(`#${category}-row`).append(`
                <div class="col-4">
                                <div class="d-flex m-2">
                                    <input class="pe-0 btn-check" type="checkbox" name="pack-items" id="item-${item.id}-checkbox" value="${item.name}">
                                    <label class="btn btn-outline-secondary" for="item-${item.id}-checkbox"}>${item.name}</label>
                                </div>
                            </div>`)
                }
            }
            
    }

    $createPackBtn.toggleClass('visually-hidden')
    $itemSectionBtn.toggleClass('visually-hidden')

    $('#confirm-items-button').on('click', (e) => {
        e.preventDefault()
        $('#confirm-items-button').toggleClass('visually-hidden')
        $('#create-pack-button').toggleClass('visually-hidden')
        $packSection.toggleClass('visually-hidden')
        $('#item-section').toggleClass('visually-hidden')
    })

})