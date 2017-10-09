/**
 * Created by wesselklijnsma on 07-10-17.
 */
function initMap() {
//        var csv = readTextFile("/Users/wesselklijnsma/Documents/CLS/Large-scale_data_enigeering/visualization/ships.csv");
//        var ships = $.csv.toObjects(csv);
    //  48.746792, 4.493420
    var center = {lat: 48.746792, lng: 4.493420};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: center
    });
    var markers = [];

    function addShip(ship) {
        var loc = {lat: ship.lat, lng: ship.lng};
        var contentString = '<div id="content">' +
            '<div id="siteNotice">' +
            '</div>' +
            '<h1 id="firstHeading" class="firstHeading">' + ship.mmsi + '</h1>' +
            '<div id="bodyContent">' +
            '</div>' +
            '</div>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });

        var marker = new google.maps.Marker({
            position: loc,
            map: map,
            title: ship.mmsi
        });
        markers.push(marker);
        marker.addListener('click', function () {
            infowindow.open(map, marker);
        });
        //markers = markers.push(marker);
        //console.log("ship_added")
    }

    function setMapOnAll(map) {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(map);
        }
    }

    // Removes the markers from the map, but keeps them in the array.
    function clearMarkers() {
        setMapOnAll(null);
        markers = [];
    }

    var days;
    $.getJSON("http://127.0.0.1:8080/positions.json", function (data) {
        var groups = Object.create(null);
        for (var i = 0; i < data.length; i++) {
            var item = data[i];

            if (!groups[item.date]) {
                groups[item.date] = [];
            }

            groups[item.date].push({
                mmsi: item.mmsi,
                lat: parseFloat(item['avg(lat)']),
                lng: parseFloat(item['avg(lng)'])
            });
        }
        var result = [];

        for (var x in groups) {
            var obj = {};
            obj[x] = groups[x];
            result.push(obj);
        }

        plot_ships(result, 0);
        days = result;
    });

    function plot_ships(days, index) {
        var day = days[index];
        for (var d in day) {
            //console.log(d);
            for (var i = 0; i < day[d].length; i++) {
                addShip(day[d][i])
            }
        }
    }

    var counter = 1;
    $(document).keypress(function () {
        clearMarkers();
        if (counter < days.length) {
            plot_ships(days, counter);
            counter += 7;
            updateWindow(days[counter])
        } else {
            //alert('starting over');
            counter = 0;
            plot_ships(days, counter);
            updateWindow(days[counter])
        }
    });

    function updateWindow(date) {
        //var start_date = date.replace(/\//g, '-');
        var start_date = Object.keys(date)[0].replace(/\//g, '-');
        var end_date1 = new Date(start_date);
        end_date1.setDate(end_date1.getDate() + 3);
        var end_date = end_date1.toISOString();

        console.log(start_date);
        console.log(end_date);
        var update = {
            shapes: [
                {
                    type: 'rect',
                    // x-reference is assigned to the x-values
                    xref: 'x',
                    // y-reference is assigned to the plot paper [0,1]
                    yref: 'paper',
                    x0: start_date,
                    y0: 0,
                    x1: end_date,
                    y1: 1,
                    fillcolor: '#FF5733',
                    opacity: 0.6,
                    line: {
                        width: 0
                    }
                }
            ]
        };
        Plotly.relayout(document.getElementById('wind-speed'), update)
        Plotly.relayout(document.getElementById('oil-price'), update)

    }

    //d3.json('http://127.0.0.1:8080/sample.json', function (error, dataset) {
    //    dataset.forEach(function (d) {
    //            d.lng = parseFloat(d.lng);
    //            d.lat = parseFloat(d.lat);
    //            d.cog = parseFloat(d.cog);
    //            addShip(d);
    //        });
    //    json_data = dataset;
    //    console.log(dataset)
    //});
}






