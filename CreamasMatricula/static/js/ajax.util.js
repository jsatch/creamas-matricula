//***** Constantes *****

var OK = 1;
var ERROR = 0;

//**** Metodos de la Aplicaci\u00f3n *****



function listar(entidad){
	
	var html="";
	var colspan=0;
	var dataTable=true;
	var data = null;

	if(entidad=='puntoVenta')	colspan=6;
	if(entidad=='usuario')		colspan=4;
	if(entidad=='producto')		colspan=3;
	if(entidad=='giroParametro')		colspan=3;

	//Mostrando icono de 'loading'
	$('#data-'+entidad).html("<tr><td colspan='"+colspan+"' align='center'><img src='../static/images/loading.gif' /></td></tr>");


	//var letra=entidad.substring(0,1).toUpperCase();
	var accion="listar_" + entidad;

	doAjax(accion, data, 'POST', function(resp){
		if(resp){
			var mensaje = resp.mensaje;
			if(mensaje == ''){
				if(entidad=='matricula'){
					var data = resp.lista_matriculas;
					this.matricula=data;
					for(var i = 0; i<data.length; i++){	
						html+="<tr id="+data[i].idmatricula+">";
						var alumno = data[i].alumno;
						if(alumno==null)	alumno="-";
						html+="<td>"+alumno+"</td>";
						var grado = data[i].grado;
						if(grado==null) 
							grado="-";
						else provider="-";
						html+="<td>"+grado+"</td>";
						html+="<td>"+data[i].seccion+"</td>";
						html+="<td>"+data[i].taller+"</td>";
						html+="<td>"+data[i].email+"</td>";
						html+="<td><a href='/matricula-registrar/"+ data[i].idmatricula +"' > <img title='Editar' src='../static/images/edit.png'></a> <a href='/matricula-eliminar/"+ data[i].idmatricula +"' ><img title='Eliminar' src='../static/images/delete.png'></a></td>";
						html+="</tr>";
					}
					if(data.length==0){
						dataTable=false;
						html="<tr><td colspan='"+colspan+"' align='center' style='color: red;'><img src='../static/images/error.jpg'  width='15' >No hay ninguna matricula registrada</td></tr>";
					}
				}
			}else{
				html="<tr><td colspan='"+colspan+"' align='center' style='color: red;'><img src='../static/images/error.jpg'  width='15' >"+mensaje+"</td></tr>";
				dataTable=false;
			}
			$('#data-'+entidad).html(html);
			if(dataTable){
				if(entidad=="puntoVenta"){
					var table=$(".formato-tabla").dataTable({
						"oLanguage": {
			                "sUrl": "../static/javascript/language.txt"
						},
		                "bSort": false,
		                "aLengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
		                "fnDrawCallback": function( oSettings ) {
		                	puntosDeVentaFiltrados=puntosDeVenta;
		                	var filteredData = fnGetFilteredData(table);
      						actualizarPuntosEnMapa(filteredData, puntosDeVenta);
    					}
					});

					//Poniendo el filtro con SelectBoxes
					 $("tfoot th").each( function ( i ) {
					 	if(i==3 || i==5){
				        	this.innerHTML = fnCreateSelect( table.fnGetColumnData(i) );
					        $('select', this).change( function () {
					            table.fnFilter( $(this).val(), i );
					        } );
					    }
				    } );


				}else{
					$(".formato-tabla").dataTable({
					"oLanguage": {
		                "sUrl": "../static/javascript/language.txt"
					},
	                "bSort": false,
	                "aLengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]]
				});
				}

				
			}
			
		}
	}, 
		function(e){
			html="<tr><td colspan='"+colspan+"' align='center'>Ocurri\u00f3 un error al obtener la lista.</td></tr>";
			$('#data-'+entidad).html(html);
			if(entidad=='puntoVenta')eliminarPuntosEnMapa();
		});	
}


