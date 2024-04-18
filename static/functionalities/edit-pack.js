const $itemSectionBtn = $('#item-section-button')
const $packSection = $('#pack-section')
const $existingItemsNode = $('.item-name')
const existingItems = [];

for (let item of $existingItemsNode){
    existingItems.push(item.innerText);
}

let categories = new Set()



async function getCategories()  {
    /**Get a list of the categories available from the items database, push them to the categories Set, and return item list */
    let resp = await axios.get(`/items`)
    let items = resp.data.items    

    for(let item of items) {
       categories.add(item.category)
    }

    return(resp.data.items)
}



$itemSectionBtn.on('click', async (e)=>  {
/**Call getCategories and creates HTML lists, then assigns them to their respective categories. */
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
                    <input class="form-check-input me-1" name="pack-items" type="checkbox" id="item-${item.id}-checkbox" value="${item.name}"></input>
                    <label class="form-check-label" for="${item.id}-checkbox">${item.name}</label>
                    </li>`)

                }
                
            }
            
    }
    
    for(let existingItem of existingItems){
        for( let item of items){
            if(existingItem === item.name){
                let $match = $(`#item-${item.id}-checkbox`)
                $match.attr('checked', true);
            }
        }
    }


    $packSection.toggleClass('visually-hidden')
    $itemSectionBtn.toggleClass('visually-hidden')

    $('#item-section').after('<button id="confirm-items-button">Add Items</button')

    $('#confirm-items-button').on('click', (e) => {
        e.preventDefault()
        $('#confirm-items-button').toggleClass('visually-hidden')
        $('#update-pack-button').toggleClass('visually-hidden')
        $packSection.toggleClass('visually-hidden')
        $('#item-section').toggleClass('visually-hidden')
    })

})

//Select existing HTML LI's
// Get database LI's
// Compare the contents of both
// If existing LI is in database already >> checked
// Else >> not checked
// Make sure not to submit duplicate of exisitng items >> maybe PATCH??