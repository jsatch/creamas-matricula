var puntosEnMapa = new Array();

function mostrarPuntosDeVenta(){

	var puntosDeVenta=this.puntosDeVentaFiltrados;

	if(puntosDeVenta!=null){
    if(eraseall){
      //Si ocurre un cambio 
      eliminarPuntosEnMapa();
    }

    if(puntosDeVenta!=undefined){
  		for(var k = 0; k<puntosDeVenta.length; k++){
        var mensaje = buildInfo(puntosDeVenta[k]);
  			showPoint(puntosDeVenta[k].longitud,puntosDeVenta[k].latitud, mensaje, puntosDeVenta[k].privado);
  		}
    }

	}
  showHidemarkers(map.getZoom());
}

function geocoding(address) {
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
        }
    });
}

function reverseGeocoding(location) {

        geocoder.geocode({'latLng': location}, function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
            if (results[1]) {
              var direccion = results[0].formatted_address;
              $('#direccion').val(direccion);
            }
          } 
        });
      }

function showHidemarkers(zoom){
  if(zoom>=15){
    isMarkerListShown=true;
  }else{
    isMarkerListShown=false;
  }
  for(var i=0; i<puntosEnMapa.length; i++){
    puntosEnMapa[i].setVisible(isMarkerListShown);
  }
}

function showPuntoSinInfo(location, isGeocoding) {
    $('#longitud').val(location.lng());
    $('#latitud').val(location.lat());
    if(punto!=null) punto.setMap(null);
    var privado = $('#privado').val();
    var icon;
    if(privado=="true")   icon="blue";
    else                icon="red";
  var marker = new google.maps.Marker({
      position: location,
      map: map,
      animation: google.maps.Animation.DROP,
      icon:"http://maps.google.com/mapfiles/ms/icons/"+icon+"-dot.png"
  });
  if(isGeocoding) reverseGeocoding(location);
  punto=marker;
}

function createInfoWindow(mensaje){
    var infowindow = new google.maps.InfoWindow({content: mensaje});
    return infowindow;
}

function eliminarPuntosEnMapa(){
  for (var i = 0; i < puntosEnMapa.length; i++ ) {
    puntosEnMapa[i].setMap(null);
  }
  puntosEnMapa=new Array();
}

function showDensidad(puntosDeVenta){
  $('#mensaje').html("<img src='../images/loading.gif' /> Mostrando densidad...");
  pointArray = new google.maps.MVCArray(puntosDeVenta);
  var gradient = [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(255, 0, 0, 1)'
  ];

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray,
    gradient: gradient
  });

  heatmap.setMap(map);
  $('#mensaje').html("");
}

function showPoint(longitud, latitud,mensaje, privado){
    var infoWindow=createInfoWindow(mensaje);
    var point = new google.maps.LatLng(latitud, longitud);
    var icon;
    if(privado) icon="blue";
    else        icon="red"; 
	var marker = new google.maps.Marker({
        map:this.map,
        draggable:false,
        animation: google.maps.Animation.DROP,
        position: point,
        icon:"http://maps.google.com/mapfiles/ms/icons/"+icon+"-dot.png"
    });
    puntosEnMapa.push(marker);
    google.maps.event.addListener(marker, 'click', function(){ 
                                                                infoWindow.open(this.map,marker);
                                                            });
}

function buildInfo(entidad){
    var productos = entidad.productos;
    var listaProductos="";
    for(var i = 0;i<productos.length; i++){
        listaProductos+="<li>"+productos[i].nombre+"</li>";
    }

    var mensaje='<div id="content">'+
            '<div id="siteNotice">'+
            '</div>'+
            '<h1 id="firstHeading" class="firstHeading">'+entidad.razonSocial+'</h1>'+
            '<div id="bodyContent">'+
            "<p>"+entidad.direccion+"</p>"+
            "<p>Nivel de Ventas : "+entidad.descripcionNivelVentas+"</p>"+
            "<p>Productos : </p>"+
            "<ul>"+listaProductos+"</ul>"+
            "</div>"+
            "</div>";
    return mensaje;
}

//****** Metodos No Usados ********
/**
*Metodo para que un punto en el mapa empiece a saltar
*No se está usando en la aplicación
**/
function toggleBounce(marker) {
    if (marker.getAnimation() != null) {
        marker.setAnimation(null);
    } else {
        marker.setAnimation(google.maps.Animation.BOUNCE);
    }
}

function ajustarMapaAMarcadores(marcadores, mapa){

  var limites = new google.maps.LatLngBounds();
  console.log(marcadores.length);
  for (var i = 0, LtLgLen = marcadores.length; i < LtLgLen; i++) {
    var posicion = new google.maps.LatLng (marcadores[i].latitud, marcadores[i].longitud);
    limites.extend (posicion);
  }
  mapa.fitBounds(limites);

  var zoomChangeBoundsListener = 
        google.maps.event.addListenerOnce(map, 'bounds_changed', function(event) {
          if(marcadores.length==1){
            if (this.getZoom()){
                this.setZoom(13);
            }
          }else{
            if(this.getZoom()<7){
              this.setZoom(7);
            }
          }
    });
  setTimeout(function(){google.maps.event.removeListener(zoomChangeBoundsListener)}, 2000);

}