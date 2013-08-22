function mostrar(div){
	var entidad = div.split("-");
	$("."+entidad[1]).hide();
	$("#"+div).show();
}

function regresar(entidad){
	if(entidad=='visita'){
		$('.tablas').hide();
		$('#table-data').show();
		$('#filtro-reporte').show();
	}
}

function seleccionarSelect(field, value){
	var lista = document.getElementById(field);
	var valores = $('#' +field+' option');
	for (var i=0; i<valores.length; i++){
		if (lista.options[i].value == value){
			lista.options[i].selected = true;
		}
	}
}

function seleccionarSelectVarios(field, values){
	for(var i = 0; i<values.length; i++){
		seleccionarSelect(field,values[i]);
	}
}

function crearDialogLoading(selectorMensaje){
	$(selectorMensaje).html("<img src='../images/loading.gif' />Por favor, espere...");
	$(selectorMensaje).dialog({
		autoOpen:true,
		resizable:false,
		height:160,
		modal:true,
		disabled:false,
		buttons : {},
		// para que crezca el overlay en caso la pantalla tenga scroll
		open: function(event, ui) {
			$('.ui-widget-overlay').width($(document).width());
			$('.ui-widget-overlay').height($(document).height());
		}
	});
}


function cerrarDialogLoading(selectorMensaje){
	$(selectorMensaje).dialog("destroy");
}

function crearDialogoInfo(selectorMensaje, callback) {

	$( selectorMensaje ).dialog( "option", "buttons", [{
        text: "Continuar",
        click: function() {
        	 		$(this).dialog("close"); 
        	 		if (typeof callback != "undefined" && callback)
						callback();
        		}
    }
	] );

}

function crearDialogoPregunta(selectorMensaje, callback) {
	$(selectorMensaje).dialog({
		autoOpen:true,
		resizable:false,
		height:160,
		modal:true,
		disabled:false,
		buttons : {
			"S\u00ed" : function() {
        	 		$(this).dialog("close"); 
        	 		if (typeof callback != "undefined" && callback)
						callback();
        			},
    		"Cancelar" : function(){$(this).dialog("close");}
		},
		// para que crezca el overlay en caso la pantalla tenga scroll
		open: function(event, ui) {
			$('.ui-widget-overlay').width($(document).width());
			$('.ui-widget-overlay').height($(document).height());
		}
	});
}

function limpiarForm(entidad) {
	if(entidad=='puntoVenta'){
		$('#razonSocial').val('');
		$('#ruc').val('');
		$('#longitud').val('');
		$('#latitud').val('');
		$('#email').val('');
		$('#contacto').val('');
		$('#telefono').val('');
		$('#observacion').val('');
		$('#ruc').val('');
		$('#ruc').val('');
		var selectProductos = document.getElementById("productos");
		for (var i = 0; i < selectProductos.options.length; i++) {
			selectProductos.options[i].selected = false;
		}
		document.getElementById('giro').options[0].selected = true;
		document.getElementById('nivelVenta').options[0].selected = true;
		document.getElementById('departamento').options[0].selected = true;
		$('#provincia').html('Elija Departamento...');
		$('#provincia').attr('disabled','disabled');
		$('#distrito').html('Elija Provincia...');
		$('#distrito').attr('disabled','disabled');
	}
}

/**
 * Metodo que oculta un listado y muestra el mapa y viceversa
 * @param isMapaShown : boolean que indica si el mapa est‡ siendo mostrado o no
 */
function verMapa(isMapaShown){
	$(".puntoVenta").hide();
	if(isMapaShown){
		//Si se esta mostrando el mapa y la lista esta oculta
		$("#list-puntoVenta").show();
		this.isMapaShown=false;
		$("#btnVerMapa").html('Cambiar a Modo Mapa');
		if(isPointDisplayed){
			mostrarPuntosDeVenta();
			isPointDisplayed=false;
		}
	}else{
		//Si se esta mostrando la lista y el mapa esta oculto
		$("#mapa-puntoVenta").show();
		$("#btnVerMapa").html('Cambiar a Modo Listado');
		this.isMapaShown=true;
		if(!isMapaInit){
			initialize();
			isMapaInit=true;
		}
	}
}

function actualizarPuntosEnMapa(filteredData, puntos){
    var nuevosPuntosDeVenta=new Array();

    //if(isMapaInit){
	    if(puntos.length!=filteredData.length){
	    	for(var i=0; i<filteredData.length; i++){
	    		for(var j=0; j<puntos.length; j++){
	    			if(filteredData[i].id==puntos[j].idPuntoVenta){
	    				nuevosPuntosDeVenta.push(puntos[j]);
	    				break;
	    			}
	    		}
	    		
	    	}
	    	puntosDeVentaFiltrados=nuevosPuntosDeVenta;
	    }
		if(isMapaInit)
			mostrarPuntosDeVenta();
	//}
}

//********** DataTable script para obtener registros visibles luego de filtro *****************

function fnGetFilteredData(a){
	var anRows = [];
	for ( var i=0, iLen=a.fnSettings().aiDisplay.length ; i<iLen ; i++ ){
		var nRow = a.fnSettings().aoData[ a.fnSettings().aiDisplay[i] ].nTr;
		anRows.push( nRow );
	}
	return anRows;
}

//*********************************************************************************************

//**********Datatable script para ocultar columnas **************

function fnShowHideColumn( columna, oTable ){
    var bVis = oTable.fnSettings().aoColumns[columna].bVisible;
    oTable.fnSetColumnVis( columna, bVis ? false : true );
}

//****************************************************************


/* Opcion activa del menu */
function active_menu(){
	var url = ""+window.location;
	var pagina = url.split("/");
	if(pagina[pagina.length-1]==""){
		$("#menu span .index").parent().addClass("active");
	}else{
		var name = pagina[pagina.length-1].split(".");
		var submenu = name[0].split("-");
		if(submenu.length>1){
			name[0] = submenu[0];
		}
		try{
			var lista = [];
			lista = $("#menu span").get();
	
			for(var i=0; i<lista.length;i++){
				if(name[0] == $(lista[i]).find("div").attr("class")){
					$(lista[i]).addClass("active");
					var backgroundPos = $(lista[i]).find("div").css('background-position').split(" ");
					var xPos = backgroundPos[0];
					
					$(lista[i]).find("div").css('backgroundPosition', xPos+" -24px");
				}
			}
		}catch(e){
		
		}
	}
}


$(document).ready(function(){
	active_menu();
	$(".active").parent().find(".submenu").show();

	/* Manejo de Submenus */
	$("#menu span").click(function(){
		if($(this).parent().find(".submenu") != null){
			if($(this).parent().find(".submenu").is(":hidden")){
				//$(".submenu").css("display","none");
				$(this).parent().find(".submenu").slideDown(500).show();
			}else{
				$(this).parent().find(".submenu").slideUp(500);
			}
		}else{
			$(this).find("a").trigger("click");
		}
	});
	
	/* Efecto menu - hover */
	if (/Firefox[\/\s](\d+\.\d+)/.test(navigator.userAgent)){
		$("#menu span").mouseenter(function(){
			var backgroundPos = $(this).find("div").css('background-position').split(" ");		
			var xPos = backgroundPos[0];
			
			$(this).find("div").css('backgroundPosition', xPos+" -24px");
		}).mouseleave(function(){
			if($(this).attr("class") != "active"){
				var backgroundPos = $(this).find("div").css('background-position').split(" ");
				
				var xPos = backgroundPos[0];
		
				$(this).find("div").css('backgroundPosition', xPos+" 0px");
			}
			
		});
	}
});

