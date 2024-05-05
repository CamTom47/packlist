$('document').ready(() => {
    $('head').append(`<script>
    let autocomplete;
    function initAutocomplete()  {
        autocomplete = new google.maps.places.Autocomplete(
            document.getElementById('location'),
            {
                types: ['establishment'],
                componentRestrictions: {'country': ['US']},
                fields: ['name','place_id']
            });
            
            
            autocomplete.addListener('place_changed', onPlaceChanged);
        }
        
        $locationInput = $("#location")

        $locationInput.attr('placeholder', "Enter a location")

    function onPlaceChanged() {
        let place = autocomplete.getPlace();
        
            //Display details about the valid place
            $locationInput.attr("value", place.place_id);

            getLatLong(place)
    }

        </script> 
        <script 
        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBgdY21omysISJ--jQIkHTCsreCZPxTR8w&loading=async&libraries=places&callback=initAutocomplete" async defer>
        </script>`)
        

    })
    
    async function getLatLong(place){
        let resp = await axios.get(`https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBgdY21omysISJ--jQIkHTCsreCZPxTR8w&place_id=${place.place_id}`)
        let lat = (resp.data.results[0].geometry.location.lat)
        let lng = (resp.data.results[0].geometry.location.lng)

        $("#form-fields").append(`<input id="lat" name="lat" value="${lat}" type="hidden" />  <input id="lng" name="lng" value="${lng}" type="hidden" />`)
        }
