const $itemSectionBtn = $('#item-section-button')
const $packSection = $('#pack-section')

let categories = new Set()

async function getCategories()  {
    let resp = await axios.get(`/items`)
    let items = resp.data.items    

    for(let item of items) {
       categories.add(item.category)
    }

    return(resp.data.items)
}

$itemSectionBtn.on('click', async (e)=>  {
    e.preventDefault()
    let items = await Promise.resolve(getCategories())

    $packSection.after('<div id="item-section"></div>')

    for(let category of categories){
        $('#item-section').append(`
        <div class="pt-5">
            <ul class="list-group">
                <h3 id='${category}-h3'>${category}</h3>
            </ul>
        </div>`)

        for(let item of items){
            if(item.category === category){
                $(`#${category}-h3`).after(
                    `<li class="fw-5 fs-5 list-group-item">
                        <input class="form-check-input me-1" name="pack-items" type="checkbox" id="${item.name}Checkbox" value="${item.name}"></input>
                        <label class="form-check-label" for="${item.name}Checkbox">${item.name}</label>
                </li>`)
                
            }
        }
    }
    $packSection.toggleClass('visually-hidden')
    $itemSectionBtn.toggleClass('visually-hidden')

    $('#item-section').after('<button id="confirm-items-button">Add Items</button')

    $('#confirm-items-button').on('click', (e) => {
        e.preventDefault()
        $('#confirm-items-button').toggleClass('visually-hidden')
        $('#create-pack-button').toggleClass('visually-hidden')
        $packSection.toggleClass('visually-hidden')
        $('#item-section').toggleClass('visually-hidden')
    })

})


//     console.log('clicking')
//     // h3 = document.createElement('h3')
//     // div = document.createElement('div')
//     // ul = document.createElement('ul')
//     // li = document.createElement('li')

//     $packSection.append('<div></div>').append('<h3></h3>')

    
// })