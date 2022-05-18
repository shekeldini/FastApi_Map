var map = L.map('map').fitWorld();

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
map.setView(new L.LatLng(52.61558902526749, 83.57275390625), 7);

var markers = L.markerClusterGroup()


$.getJSON("static/files/districts.json", function(json) {
    for(district of json){
        var name = district.name
        var coordinates = district.coordinates
        var id_district = district.id
        for (coord of coordinates){
            var polygon = L.polygon(coord, {
                color: "#4747A1",
                "name": name,
                "id_district": id_district
            });
            polygon.bindTooltip(name,
               {permanent: false, direction: "center"}
            ).openTooltip()
            polygon.addTo(map);
            polygon.on('click', async function () {
                deleteLayers(L.Marker);
                var schools = await getSchools(this);
                for (school of schools){
                    if (school.coordinates != ""){
                        create_marker(school, this.options.name);
                    };
                markers.addTo(map)
                };
            });
        };
    };
});

function getSchools(polygon){
    send_data = {
        year: 2022,
        id_district: polygon.options.id_district
    }
    return $.ajax({
        type : 'GET',
        url : "oo/get_all_by_year_and_id_district",
        data: send_data
    });
};

async function create_marker(data, district_name){
    var coordinates = data.coordinates.split(";").map(str => parseFloat(str));
    var iconOptions = {
            iconUrl: '/static/images/school.png',
            iconSize: [50, 50]
         }
    var customIcon = L.icon(iconOptions);
    var marker = L.marker(coordinates, {
        "id_oo": data.id_oo,
        "oo_login": data.oo_login,
        'year': data.year,
        "oo_login": data.oo_login,
        "oo_name": data.oo_name,
        "oo_address": data.oo_address,
        "director": data.director,
        "email_oo": data.email_oo,
        "phone_number": data.phone_number,
        "coordinates": data.coordinates,
        "url": data.url,
        "district_name": district_name,
	"icon": customIcon
    });

    var text =
            "<p class='district'>" + marker.options.district_name + "</p>" +

            "<div class='block'>" +
                        "<div>" + 'Наименование' + "</div>" +
                        "<div class='name'>" + marker.options.oo_name + "</div>" +
                "</div>" +
            "<p class='name'>" + marker.options.oo_name + "</p>" +
            "<p class='address'>" + marker.options.oo_address +"</p>" + 
            "<p class='director'>" + marker.options.director +"</p>" + 
            "<p class='oo'>" + marker.options.email_oo +"</p>" + 
            "<p class='phone'>" + marker.options.phone_number +"</p>" + 
            "<a class='url'>" + marker.options.url +"</a>";

    marker.bindPopup(text, {autoClose:false}).openPopup();

    marker.on('click', function(){
        console.log(this.options);
        marker.openPopup();
    });

    markers.addLayer(marker);
};

function deleteLayers(LayerType){
    markers.eachLayer(async function(layer) {
        if (layer instanceof LayerType){
            markers.removeLayer(layer);
        };
    })
};
