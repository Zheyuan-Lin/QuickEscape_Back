document.getElementById('flightForm')
    .addEventListener('submit', async (event) => {
    event.preventDefault();

    const flightData = {
        sourceAirportCode: document.getElementById('sourceAirportCode').value,
        destinationAirportCode: document.getElementById('destinationAirportCode').value,
        date: document.getElementById('date').value,
        numAdults: document.getElementById('numAdults').value,
        numSeniors: document.getElementById('numSeniors').value,
        sortOrder: document.getElementById("sortOrder").value,
        classOfService: document.getElementById("classOfService").value,
        pageNumber: document.getElementById("pageNumber").value,
        nonstop: document.getElementById("nonstop").value,
        currencyCode: document.getElementById("currencyCode").value
    };
    try {
        const response = await axios.post('http://localhost:8080/flights/oneway', flightData);
        console.log(response.data);
        //displayFlightResults(response.data);
    } catch (error) {
        console.error('Error fetching flight data:', error);
        document.getElementById('flights').textContent = 'Error fetching flight data';
    }
});
