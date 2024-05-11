async function getItemInformation(searchItem){
    let resp = await axios.get('/api/items')
    let items = resp.data.items

    for (let item of items){
        if(item.name === searchItem)
        return item
    }
}


$('.item-label').on('click', async (e)=>{
    if (e.target.tagName === "LABEL")  {
        let item = e.target.innerText
        let foundItem = await Promise.resolve(getItemInformation(item))
        showItemInformation(foundItem)
        handleCheckUI(foundItem)

    }
})


function showItemInformation(item){
    $('#item-details').empty()
    $('#item-details').append(`
    <div class="col-6 position-fixed">
            <div id="item-card" class="card text-bg-dark">
        <div class="card-body">
        <h3 class="card-title">${item.name}</h3>
        <span class="fw-bold pe-3 fs-5">Category:</span><p>${item.category}</p>
        <span class="fw-bold pe-3 fs-5">Essential:</span><p>${item.essential}</p>
        <span class="fw-bold pe-3 fs-5">Rain:</span><p>${item.rain_precautionary}</p>
        <span class="fw-bold pe-3 fs-5">Cold:</span><p>${item.cold_precautionary}</p>
        <span class="fw-bold pe-3 fs-5">Heat:</span><p>${item.heat_precautionary}</p>
        <span class="fw-bold pe-3 fs-5">Emergency:</span><p>${item.emergency_precautionary}</p>
    </div>
    </div>

    </div>
`)
}

function handleCheckUI(item){
    $(":checked").prop('checked', false)
    $(`#${item.id}-checkbox`).prop('checked', true)
}


            