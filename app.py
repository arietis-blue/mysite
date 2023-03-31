import sys
import webview
import math
import requests
import json
 
URL = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
API_KEY = 'e96ca921135d305a'
class Nres:
    EARTH_RADIUS = 6378150
    # def __init__(self):
    #     self=self

    def move(self, distance=0, heading=0):
        # 緯線上の移動距離
        latitude_distance = distance * math.cos(math.radians(heading))

        # 1mあたりの緯度
        earth_circle = 2 * math.pi * self.EARTH_RADIUS
        latitude_per_meter = 360 / earth_circle

        # 緯度の変化量
        latitude_delta = latitude_distance * latitude_per_meter
        new_latitude = self.latitude + latitude_delta

        # 経線上の移動距離
        longitude_distance = distance * math.sin(math.radians(heading))

        # 1mあたりの経度
        earth_radius_at_longitude = self.EARTH_RADIUS * math.cos(math.radians(new_latitude))
        earth_circle_at_longitude = 2 * math.pi * earth_radius_at_longitude
        longitude_per_meter = 360 / earth_circle_at_longitude

        # 経度の変化量
        longitude_delta = longitude_distance * longitude_per_meter

        return [new_latitude, self.longitude + longitude_delta]


    def res(self,lat,lng):
        # there=[self.move(distance=30, heading=45),self.move(distance=30, heading=315),self.move(distance=30, heading=135),self.move(distance=30, heading=225)]

        body = {
            'key':API_KEY,
            'lng':lng,
            'lat':lat, 
            'range':1,
            'count':10,
            'order':4,
            'format':'json',
        }
        resta = requests.get(URL,body)
        # // 取得したデータからJSONデータを取得
        datum = resta.json()
        # // JSONデータの中からお店のデータを取得
        stores = datum['results']['shop']
        # // お店のデータの中から、店名を抜き出して表示させる
        store_list=[]
        for store_name in stores:
            restaurant={}
            restaurant['name']=store_name['name']
            restaurant['lat']=store_name['lat']
            restaurant['lng']=store_name['lng']
            restaurant['url']=store_name['urls']['pc']
            store_list.append(restaurant)
        response = json.dumps(store_list)
        return response

def get_html():
    html_str = """
     
    <!DOCTYPE html>
    <html>
    <head lang="en">
    <meta charset="UTF-8">
     
    <style>
        #response-container {
            display: none;
            padding: 3rem;
            margin: 2rem 2rem;
            font-size: 100%;
            border: 2px dashed #ccc;
        }
     
        label {
            margin-left: 0.3rem;
            margin-right: 0.3rem;
        }
     
        button {
          display: inline-block;
          text-decoration: none;
          color: #FFF;
          width: 100%;
          height: 40px;
          font-weight:bold;

          text-align: center;
          overflow: hidden;
          background-image: linear-gradient(45deg, #709dff 0%, #91fdb7 100%);
          transition: .4s;
        }
         

                     
    </style>
    </head>
    <body>
    <script>
        var resmarker=[];
        let map;


        window.initMap = function () {
            var latlng = new google.maps.LatLng(35.681263, 139.767937);
            map = new google.maps.Map(document.getElementById('map'), {
                center: latlng,
                zoom: 15
            });
            marker = new google.maps.Marker({
                map: map, 
                position: latlng,
            });

            // クリックイベントを追加
            map.addListener('click', function(e) {
            getClickLatLng(e.latLng, map);
            });
        }

        function getClickLatLng(lat_lng, map) {
            map.panTo(lat_lng);
            marker.setMap(null);
            marker = null;
            if (!(typeof resmarker === 'undefined')){
                for (var i = 0; i < resmarker.length; i++) {
					resmarker[i].setMap(null);
			    }
                resmarker = [];
            };

            marker = new google.maps.Marker({
                map: map, position: lat_lng 
            });
            infoWindow = new google.maps.InfoWindow({
                content: '周辺の人気レストランを検索'
            });
            var btn = document.createElement("button");
            btn.innerText = "周辺の人気レストランを検索する";
            infoWindow.setContent(btn);
            google.maps.event.addDomListener(btn,"click", function(){
                search(lat_lng)
            });
            markerEvent();
        };
        function markerEvent() {
            marker.addListener('click', function() {
                infoWindow.open(map, marker);
            });
        }

        function search(lat_lng){
            let lat=lat_lng.lat();
            let lng=lat_lng.lng();
            pywebview.api.res(lat,lng).then(get_return_from_python);
        }
        function get_return_from_python(response) {          
            data=JSON.parse(response)
            var resinfoWindow=[];
            for (let loc in response) {
                var reslatlng = new google.maps.LatLng(data[loc]['lat'], data[loc]['lng']);
                resmarker[loc] = new google.maps.Marker({
                    map: map, 
                    position: reslatlng,
                });
                resinfoWindow[loc] = new google.maps.InfoWindow({
                    content: data[loc]['name']
                });

                resmarkerEvent(loc);
            } 
        function resmarkerEvent(i) {
            resmarker[i].addListener('click', function() {
                resinfoWindow[i].open(map, resmarker[i]);
                target = document.getElementById("output");
                document.getElementById("ifr").removeAttribute("src");
                document.getElementById("ifr").src = data[i]['url'];
            });
        }

        
        }
     
    </script>
    <div style="width:100%;height:320px;" id="map"></div>
    <script
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA4zY3aG8C9JxD0wkFcysfKIkVqW79CHJg&callback=initMap&v=weekly"
    defer
    ></script>
    <div id="output"><iframe src="" id="ifr" width="100%" height="600" scrolling="auto" frameborder="0"></iframe></div>
    </iframe>
    </body>
    </html>
    """
    return html_str
 
                    #  content: loc['name'] + </br> + loc['url']
if __name__ == '__main__':
    # GUI
    html = get_html()
    # 関数
    api = Nres()
    window = webview.create_window('周辺300m以内の飲食店からおすすめ10個を選出', html=html, js_api=api, height=400)
    webview.start()

    # +"<br>"+"<a href="+data[loc]['url']+"target='_self'rel='noopener noreferrer'>ホットペッパーリンク</a>"