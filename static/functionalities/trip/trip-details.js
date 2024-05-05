let $isoDatesNodes = $('.trip-date')

function convertNodesToArray(nodes)  {

    let isoDates = []
    for (let node of nodes)  {
        isoDates.push(node.innerText)
    }
    return isoDates
}

let isoDates = convertNodesToArray($isoDatesNodes)

function convertTripDate(isoDate)  {
    let convertedDate = new Date (isoDate)
    return convertedDate
}


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
        idx += 1
    }

}

function parseDate(date)  {
    let dateString = date.toDateString().split(' ')
    let dateInfo = {
        "day": dateString[0],
        "month": dateString[1],
        "date": dateString[2]
    }

    return dateInfo
}

function parseTime(date)  {
    let timeString = date.toLocaleTimeString()
    return timeString
}


function assignIdxToDateDivs(){
    let idx = 0;
    for(let isoDateDiv of $isoDatesNodes){
        isoDateDiv.setAttribute('id',`date-${idx}`)
        idx += 1
    }}

$('window').ready( ()=>{
    assignIdxToDateDivs()
    updateIsoDateHTML(isoDates)
    updateSunriseHTML()
    // updateSunsetHTML()
})


function updateSunriseHTML(){
let $sunriseNodes = $('.sunrise-p')
let sunriseDates = convertNodesToArray($sunriseNodes)
console.log(sunriseDates)
for(let sunriseDate in sunriseDates){
    formattedDate = convertTripDate(sunriseDate)
    let sunriseInfo = parseTime(formattedDate)
    console.log(sunriseInfo)
}

}
function updateSunsetHTML(){


}