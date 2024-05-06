const $itemSection = $('#item-section')
const $essentialSection = $('#essential_section')
const $heatSection = $('#heat-section')
const $coldSection = $('#cold-section')
const $rainSection = $('#rain-section')
const $emergencySection = $('#emergency_section')
const $existingItemsNode = $('.item-name')

const existingItems = [];

for (let item of $existingItemsNode){
    existingItems.push(item.innerText);
}

$('document').ready(() =>{
   
for(let existingItem of pack_items){
    for( let item of essential_items){
        if(existingItem !== item){
            $essentialSection.after(
                `<li class="fw-5 fs-5 list-group-item">
                <input class="form-check-input me-1" name="pack-items" type="checkbox" id="item-${item.id}-checkbox" value="${item.name}"></input>
                <label class="form-check-label" for="${item.id}-checkbox">${item.name}</label>
                </li>`).after('<button id="essential-items-button" class="btn btn sucess">Next</button>')

        }
    }
}

    for(let existingItem of pack_items){
    for( let item of heat_items){
        if(existingItem !== item){
            $heatSection.after(
                `<li class="fw-5 fs-5 list-group-item">
                <input class="form-check-input me-1" name="pack-items" type="checkbox" id="item-${item.id}-checkbox" value="${item.name}"></input>
                <label class="form-check-label" for="${item.id}-checkbox">${item.name}</label>
                </li>`).after('<button id="heat-items-button" class="btn btn sucess">Next</button>')

        }
    }
    }

    for(let existingItem of pack_items){
    for( let item of cold_items){
        if(existingItem !== item){
            $coldSection.after(
                `<li class="fw-5 fs-5 list-group-item">
                <input class="form-check-input me-1" name="pack-items" type="checkbox" id="item-${item.id}-checkbox" value="${item.name}"></input>
                <label class="form-check-label" for="${item.id}-checkbox">${item.name}</label>
                </li>`).after('<button id="cold-items-button" class="btn btn sucess">Next</button>')

        }
    }
    }

    for(let existingItem of pack_items){
    for( let item of rain_items){
        if(existingItem !== item){
            $rainSection.after(
                `<li class="fw-5 fs-5 list-group-item">
                <input class="form-check-input me-1" name="pack-items" type="checkbox" id="item-${item.id}-checkbox" value="${item.name}"></input>
                <label class="form-check-label" for="${item.id}-checkbox">${item.name}</label>
                </li>`).after('<button id="rain-items-button" class="btn btn sucess">Next</button>')

        }
    }
    }

    for(let existingItem of pack_items){
    for( let item of emergency){
        if(existingItem !== item){
            $emergencySection.after(
                `<li class="fw-5 fs-5 list-group-item">
                <input class="form-check-input me-1" name="pack-items" type="checkbox" id="item-${item.id}-checkbox" value="${item.name}"></input>
                <label class="form-check-label" for="${item.id}-checkbox">${item.name}</label>
                </li>`).after('<button id="emergency-items-button" class="btn btn sucess">Next</button>')
        }
    }
    }

})

$itemSection.on('click')