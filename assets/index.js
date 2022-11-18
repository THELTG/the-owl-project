$(document).ready(()=>{
    console.log('showing reading time now')
    function refreshTime() {
        var dateString = new Date().toLocaleString();
        var formattedString = dateString.replace(", ", " - ");
        $("#time-display").html(formattedString)
    }
    setInterval(refreshTime, 1000);
})