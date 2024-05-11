let $isoDatesNodes = $('.trip-date')
let $sunriseNodes = $('.sunrise-p')
let $sunsetNodes = $('.sunset-p')




// Convert jQuery nodes into an array
function convertNodesToArray(nodes)  {
    let isoDates = []
    for (let node of nodes)  {
        isoDates.push(node.innerText)
    }
    return isoDates
}

let isoDates = convertNodesToArray($isoDatesNodes)


// Create a Date object from the isoDate
function convertTripDate(isoDate)  {
    let convertedDate = new Date (isoDate)
    return convertedDate
}

// Create a date object and return the time
function convertTripDateTime(date)  {
    let convertedDate = new Date (date)
    let hours = convertedDate.getHours()
    let minutes = convertedDate.getMinutes()

    let sunriseTime = {
        "hours": hours,
        "minutes": minutes
    }

    return sunriseTime
}


// Get formatted date objects back from iso dates and update HTML
function updateIsoDateHTML(isoDates){
    let idx = 0;
    for(let date of isoDates){
        let newFormat = convertTripDate(date)
        let dateInfo = parseDate(newFormat)
        $(`#date-${idx}`).empty()
        $(`#date-${idx}`).append(`<div>
        <p>
        ${dateInfo['day']}
        ${dateInfo['month']}
        ${dateInfo['date']}
        </p>
        </div>`)
        idx++ 
    }

}

// Split the date object into a javascript object
function parseDate(date)  {
    let dateString = date.toDateString().split(' ')
    let dateInfo = {
        "day": dateString[0],
        "month": dateString[1],
        "date": dateString[2]
    }

    return dateInfo
}

// Assign unique Ids to the new date divs
function assignIdxToDateDivs(){
    let idx = 0;
    for(let isoDateDiv of $isoDatesNodes){
        isoDateDiv.setAttribute('id',`date-${idx}`)
        idx++
    }}

$('window').ready( ()=>{
    assignIdxToDateDivs()
    assignIdxToSunriseDivs()
    assignIdxToSunSetDivs()
    updateIsoDateHTML(isoDates)
    updateSunriseHTML()
    updateSunsetHTML()
})


function updateSunriseHTML(){
let sunriseDates = convertNodesToArray($sunriseNodes)
let idx = 0
for(let sunriseDate of sunriseDates){
    let sunriseTime = convertTripDateTime(sunriseDate)
    $(`#sunrise-time-${idx}`).empty()
    $(`#sunrise-time-${idx}`).append(`<div>
    <p>
    ${sunriseTime.hours}:${sunriseTime.minutes}
    </p>
    </div>`)
    idx++

}

}

function assignIdxToSunriseDivs(){
    let idx = 0 
    for(let sunriseNode of $sunriseNodes){
        sunriseNode.setAttribute('id', `sunrise-time-${idx}`)
        idx++
    }

}

function updateSunsetHTML(){
    let sunsetDates = convertNodesToArray($sunsetNodes)
    let idx = 0
    for(let sunsetDate of sunsetDates){
        let sunsetTime = convertTripDateTime(sunsetDate)
        $(`#sunset-time-${idx}`).empty()
        $(`#sunset-time-${idx}`).append(`<div>
        <p>
        ${sunsetTime.hours}:${sunsetTime.minutes}
        </p>
        </div>`)
        idx++
    
    }
    
    }
    
    function assignIdxToSunSetDivs(){
        let idx = 0 
        for(let sunsetNode of $sunsetNodes){
            sunsetNode.setAttribute('id', `sunset-time-${idx}`)
            idx++
        }
    
    }