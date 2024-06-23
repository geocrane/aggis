function delete_user_markers() {
    if (user_markers.length > 0) {
        user_markers.forEach(
            marker => {
                map.removeLayer(marker);
            }
        )
        user_markers.splice(0, user_markers.length);
    }
}

//Функция расчета длины отрезка по заданным координатам концов
function searchLength(Xa, Ya, Xb, Yb) {
    var d = Math.sqrt((Xb - Xa) ** 2 + (Yb - Ya) ** 2);
    return d
}

//Функция для расчета точек на отрезке с указанием количества разбиений отрезка
function searchPoints(Xa, Ya, Xb, Yb, stepsCount) {
    elements = [];
    // длина отрезка между точками
    var lineLength = searchLength(Xa, Ya, Xb, Yb);
    // расстояние между граничными точками, на которые будет разбит отрезок
    var Rac = lineLength / stepsCount;
    for (let j = 1; j < stepsCount + 1; j++) {
        var k = Rac * j / lineLength;
        Xc = Xa + (Xb - Xa) * k;
        Yc = Ya + (Yb - Ya) * k;
        elements.push([Xc, Yc]);
    }
    return elements;
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const CustomIcon_1 = L.icon({
    iconUrl: "{% static 'icons/icon_1.png' %}",
    iconSize: [38, 38],
    iconAnchor: [0, 0],
    popupAnchor: [0, 0]
});

function markers(lat, lon, popup, marker_size, marker_color) {
    for (let i = 0; i < lat.length; i++) {
        var marker = L.circleMarker(
            [lat[i], lon[i]],
            {
                radius: marker_size[i],
                color: marker_color[i]
            }
        ).bindPopup(popup[i]).addTo(map);
    }
}

function polygon(lat, lon) {
    var polygon_color = 'red';
    var polygon_points = zip([lat, lon])
    var polygon = L.polygon(polygon_points, { color: polygon_color }).addTo(map);
}

function route(xa, ya, xb, yb, popup1, popup2, lineWeight, lineColor) {
    (async function main() {
        const velocity = 0.008;
        const sleepTime = 10;
        for (let i = 0; i < xa.length; i++) {
            var lineLength = searchLength(xa[i], ya[i], xb[i], yb[i]);
            var stepsCount = Math.floor(lineLength / (sleepTime * velocity));
            // находим пары точек, по которым будем отрисовывать
            var searched_points = searchPoints(xa[i], ya[i], xb[i], yb[i], stepsCount);
            let first_point = searched_points[0];
            let last_point = searched_points.at(-1);
            // добавляем первую точку на карту и открываем ее описание
            //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            //L.marker(first_point).addTo(map).bindPopup(popup1[i]).openPopup();
            L.marker(first_point, { icon: CustomIcon_1 }).addTo(map).bindPopup(popup1[i]).openPopup();
            /*
            Проходим по точкам для отрисовки. Алгоритм: добавили маркер->задержка->удалили маркер
            Такой алгоритм позволит создать иллюзию плавного передвижения одного и того же маркера
            */
            for (let j = 1; j < searched_points.length; j++) {
                ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                //let map_marker = L.marker(searched_points[j]).addTo(map);
                let map_marker = L.marker(searched_points[j], { icon: CustomIcon_1 }).addTo(map);
                await sleep(sleepTime);
                map.removeLayer(map_marker);
            }
            //добавляем на карту маркер последней точки и открываем ее описание
            /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            //L.marker(last_point).addTo(map).bindPopup(popup2[i]).openPopup();
            L.marker(last_point, { icon: CustomIcon_1 }).addTo(map).bindPopup(popup2[i]).openPopup();
            // соединяем первую и последнюю точки линией
            var latlngs = [first_point, last_point];
            var polyline = L.polyline(latlngs,
                {
                    color: lineColor[i],
                    weight: lineWeight[i]
                }
            ).addTo(map);
            await sleep(200);
        }
    })();
}

function heatMap(lat, lng, intensity, radiusParam, blurParam, maxZoomParam) {
    var heatMapParams = zip([lat, lng, intensity]);
    var heat = L.heatLayer(
        heatMapParams,
        {
            radius: radiusParam,
            blur: blurParam,
            maxZoom: maxZoomParam
        }
    ).addTo(map);
}