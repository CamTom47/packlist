function addPopoverContent()  {


    $('#essential').after(`
    <a role="button" class="fas fa-question text text-decoration-none btn btn-link link-light"
        data-bs-toggle="popover" 
        tabindex="0"
        data-bs-trigger="focus"
        data-bs-custom-class="custom-popover"
        data-bs-title="Essential"
        data-bs-content="Is this item crucial to your packpacking trip?">
</a>
`)


$('#rain_precautionary').after(`
<a role="button" class="fas fa-question text text-decoration-none btn btn-link link-light"
    data-bs-toggle="popover" 
    tabindex="1"
    data-bs-trigger="focus"
    data-bs-custom-class="custom-popover"
    data-bs-title="Rai Gear"
    data-bs-content="Does this item provide protection from the rain?">
</a>
`)


$('#cold_precautionary').after(`
<a role="button" class="fas fa-question text text-decoration-none btn btn-link link-light"
    data-bs-toggle="popover" 
    tabindex="2"
    data-bs-trigger="focus"
    data-bs-custom-class="custom-popover"
    data-bs-title="Cold Gear"
    data-bs-content="Do you need this when the temperatures get low?">
</a>
`)


$('#heat_precautionary').after(`
<a role="button" class="fas fa-question text text-decoration-none btn btn-link link-light"
    data-bs-toggle="popover" 
    tabindex="03"
    data-bs-trigger="focus"
    data-bs-custom-class="custom-popover"
    data-bs-title="Heat Item"
    data-bs-content="Is this item necessary when temperatures get too high?">
</a>
`)



$('#emergency_precautionary').after(`
<a role="button" class="fas fa-question text text-decoration-none btn btn-link link-light"
    data-bs-toggle="popover" 
    tabindex="4"
    data-bs-trigger="focus"
    data-bs-custom-class="custom-popover"
    data-bs-title="Emergency"
    data-bs-content="Is this item necessary in emergencies?">
</a>
`)
}

$('#essential').text('Essential')
$('#rain_precautionary').text('Rain Gear')
$('#cold_precautionary').text('Cold Gear')
$('#heat_precautionary').text('High Temperature Gear')
$('#emergency_precautionary').text('Emergency Item')


$('ul input').addClass('text-decoration-none')

$('.form-div').addClass('col-md-4 g-5')



$('#name-div').addClass('col-md-6 g-5')
$('#category-div').addClass('col-md-6 g-5')


$("window").ready( () =>  {
    $("#item-form").append(`<input id="removable" name="removable" value="True" type="hidden" />`)
    addPopoverContent()
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
})

const popover = new bootstrap.Popover('.popover-dismiss', {
    trigger: 'focus'
  })