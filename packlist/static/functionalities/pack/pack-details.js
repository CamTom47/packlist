function updateArrow(event)  {
    $(this).toggleClass("fa-angle-down")
    $(this).toggleClass("fa-angle-up")
}

$('#item-categories h3').on('click', "button", updateArrow) 


let selectedItems = [];
let packCount = getPackItemCount()
let currentCount = countCheckedItems()


function getPackItemCount() {
    let packCount = $(".items").length
    return packCount
}

function countCheckedItems()  {
    let $count = $(":checked").length
    return $count
}

$('window').ready(async (e) => {
    $('#pack-notes').after(`<div class="">
            <p id="item-count">Items Checked: ${currentCount} of ${packCount}</p>
    </div>`)
})



$("body input").on("click", (e) => {
    if(e.target.type === "checkbox"){

        let currentCount = countCheckedItems()
        $("#item-count").text(`Items Checked: ${currentCount} of ${packCount}`)
    }
})