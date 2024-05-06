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

    $packForm.after('<div id="item-section" class="d-inline bg-light card mt-5 me-5 w-75 pe-5"></div>')
    
    $("#item-section").append(`<div id="category-section" class="d-inline w-100 p-3"></div>`)
    
    for(let category of categories){
        $('#category-section').append(`

        <h3 class="ms-3 text-dark">
                        ${category}
                    </h3>
                    <hr>
                    <ul id="${category}">
                        <div id="${category}-row" class="row bg-secondary border rounded">
                        </div>
                        </ul>`)
                        

        for(let item of items){
            
            if(item.category === category){
                $(`#${category}-row`).append(`
                <div class="col-4">
                                <div class="d-flex m-2 card bg-light">
                                    <input class="pe-0 btn-check" type="checkbox" name="pack-items" id="item-${item.id}-checkbox" value="${item.name}">
                                    <label class="btn btn-outline-dark" for="item-${item.id}-checkbox"}>${item.name}</label>
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