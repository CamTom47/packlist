const $itemSectionBtn = $('#item-section-button')
const $packSection = $('#pack-section')
const $existingItemsNode = $('.existing-item')
const existingItems = [];

for (let item of $existingItemsNode){
    existingItems.push(item.innerText);
}

let categories = new Set()



async function getCategories()  {
    /**Get a list of the categories available from the items database, push them to the categories Set, and return item list */
    let resp = await axios.get(`/api/items`)
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

    $("#category-section").empty()

    for(let category of categories){
        $('#category-section').append(`

        <h3 class="ms-3">
                        ${category}
                    </h3>
                    <hr>
                    <ul class="" id="${category}">
                        <div id="${category}-row" class="row">
                        </div>
                        </ul>`)
                        

        for(let item of items){
            
            if(item.category === category){
                $(`#${category}-row`).append(`
                <div class="col-4">
                                <div class="d-flex">
                                    <input class="pe-0 item-checkbox" type="checkbox" name="pack-items" id="item-${item.id}-checkbox" value="${item.name}">
                                    <div class="d-flex ps-2 card card-body m-3 p-0">
                                        <li class="items list-unstyled">${item.name}</li>
                                    </div>
                                </div>
                            </div>`)
                }
            }
            
    }
    
    for(let existingItem of existingItems){
        for( let item of items){
            if(existingItem === item.name){
                console.log(item)
                console.log(existingItem)
                let $match = $(`#item-${item.id}-checkbox`)
                $match.attr('checked', true);
            }
        }
    }
    $itemSectionBtn.toggleClass('visually-hidden')

})
