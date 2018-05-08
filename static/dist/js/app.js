$(document).ready(function(e){
	//not used
	$("#user_patients").on('click', function(e){
		console.log("clicked");
		$.ajax({
			cache: false,
			url: '/user/patients',
			type: "GET",
			dataType:"html",

			success : function(result){
				document.open();
				document.write(result);
				document.close();
			},
			error: function(xhr, resp, text){
					console.log(xhr, resp, text);
			}
		})
		e.preventDefault();	
	});

	$("#search-btn").on('click', function(e){
		console.log("clicked")
		$.ajax({
			cache: false,
			url: '/search',
			type: "GET",
			data: $("#search1").serialize(),
			success : function(result){
				//$(".flex-row").apppend(result);
				//$(".flex-row").scrollLeft(10000)
				console.log("search");
			},
			error: function(xhr, resp, text){
					console.log(xhr, resp, text);
			}
		})
		e.preventDefault();	
	});
	$(document).on("click",".save", function(e){
		console.log("clicked");
		var token=sessionStorage.getItem("x-access-token")
		req=$.ajax({
			url:'/user/patients',
			type: 'POST',
			data: $(".create").serialize(),
			dataType:"json"

		});
		req.done(function(data){
			console.log("saved");
			console.log(data)
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click",".CNR", function(e){

		console.log("clicked");
		req=$.ajax({
			url:'/views/createCReport.html',
			type: 'GET',
		});
		req.done(function(data){
			console.log("cnr");
			$(".flex-row").append(data)
			$(".flex-row").scrollLeft(10000)
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});

	$(document).on("click",".CRSubmit", function(e){
		console.log($("#createmedreport"));


		req=$.ajax({
			url:'/user/medhistory',
			type: 'POST',
			data:{"diagnosis": $("#diagnosis").val(),
                "episode_number":$("#epNumber").val(),
                "institution":$("#origin").val(),
                "symptoms":$("#symptoms").val(),
                "intervention":$("#intervention").val(),
                "radiology":$("#radiology").val(),
				"patients":$(".CNR").attr("id"),
				"date":new Date().toString(),
                "origin":1
                 },
            //data: $("#createmedreport").serialize(),
		    success : function(data){
				console.log("record created");
			},
			error: function(xhr, resp, text){
					console.log(xhr, resp, text);
			}
		})

		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});


	$(document).on("click",".radH", function(e){
        var id = $(".CNR").attr("id");
		console.log("clicked");
		req=$.ajax({
			url:'/patient/'+id+'/radiology',
			type: 'GET',
		});
		req.done(function(data){
			console.log("radH");
			$(".flex-row").append(data)
			$(".flex-row").scrollLeft(10000)
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});

	$(document).on("click", ".add_patient", function(e){
		req=$.ajax({
			url:'/user/patients/addPatient',
			type: 'GET',
		});
		req.done(function(data){
			console.log("add_patient")
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
		});
	});

	$(document).on('click', "#ptable > tbody > tr", function(e){
		console.log("lll")
		var id=$(this).attr("id");
		console.log(id)
		req=$.ajax({
			url:'/user/patients/'+id,
			type: 'GET',
		});

		req.done(function(data){
			console.log("plist");
			$(".flex-row").append(data);
			$(".flex-row").scrollLeft(10000);
		});
	});

	$(document).on('click', ".rlist > tbody > tr", function(e){
		var id = 4
		req=$.ajax({
			url:'/user/patients/radiologyreport/'+id,
			type: 'GET',
		});
		req.done(function(data){
			console.log("rlist");
			$(".flex-row").append(data);
			$(".flex-row").scrollLeft(10000);
		});		
	});

	$(document).on('click', "#mhList > tbody > tr", function(e){
		var id=$(this).attr("id")
		console.log("mhlist");
		req=$.ajax({
			url:'/user/medhistory/'+id,
			type: 'GET',
		});
		req.done(function(data){
			$(".flex-row").append(data);
			$(".flex-row").scrollLeft(10000);
		});		
	});
	$(document).on('click', ".socialHistItem > tbody > tr", function(e){
		var id = $(".CNR").attr("id");
		req=$.ajax({
			url:'/user/socialhistory/'+id,
			type: 'GET',
		});
		req.done(function(data){
			console.log("socialHistItem");
			$(".flex-row").append(data);
			$(".flex-row").scrollLeft(10000);
		});		
	});

	$(document).on('click', ".famHistList > tbody > tr", function(e){
		var id = 4
		req=$.ajax({
			url:'/user/patients/familyhistory/'+id,
			type: 'GET',
		});
		req.done(function(data){
			console.log("socialHistItem");
			$(".flex-row").append(data);
			$(".flex-row").scrollLeft(10000);
		});		
	});

	$(document).on('click', "#SubmitFH", function(e){
		var id = 4
		req=$.ajax({
			url:'/user/familyhistory/',
			type: 'POST',
            data:$("#createFH").serialize()
		});
		req.done(function(data){
			console.log("socialHistItem");
			$(".flex-row").append(data);
			$(".flex-row").scrollLeft(10000);
		});
	});

	$(document).on('click', "#submit_gp", function(e){
        console.log("add_gp")
		req=$.ajax({
			url:'/admin/GP',
			type: 'POST',
            data:$("#add_gp_form").serialize()
		});
		req.done(function(data){
			console.log("socialHistItem");
			$(".flex-row").append(data);
			$(".flex-row").scrollLeft(10000);
		});
	});

	$(document).on('click', ".alist > tbody > tr", function(e){
		var id = 4
		req=$.ajax({
			url:'/user/patients/allergy/'+id,
			type: 'GET',
		});
		req.done(function(data){
			console.log("allergy");
			$(".flex-row").append(data);
			$(".flex-row").scrollLeft(10000);
		});		
	});
	
	$(document).on("click", ".add_rad", function(e){
		req=$.ajax({
			url:'/user/patients/radiologyreport/new',
			type: 'GET',
		});
		req.done(function(data){
			console.log("add_rad")
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
		});
	});

	$(document).on("click", ".med_history", function(e){
		var id =$(".CNR").attr("id")
		req=$.ajax({
			url:'/patient/'+id+'/medhistory',
			type: 'GET',
		});
		req.done(function(data){
			console.log("med_history")
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
		});
		e.preventDefault();	
	});

	$(document).on("click", ".drug_hist", function(e){
		var id = $(".CNR").attr("id")
		req=$.ajax({
			url:'/patient/'+id+'/drug_history',
			type: 'GET',
		});
		req.done(function(data){
			console.log("drug_hist")
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
		});
		e.preventDefault();	
	});

	$(document).on("click", ".add_drug", function(e){
		req=$.ajax({
			url:'/patient/drug_history',
			type: 'GET',
		});
		req.done(function(data){
			console.log("add_drug")
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
		});
		e.preventDefault();	
	});

	$(document).on("click", ".dlist > tbody > tr", function(e){
		var id = 4
		req=$.ajax({
			url:'/user/patients/historydrug/item/'+id,
			type: 'GET',
		});
		req.done(function(data){
			console.log("dlist");
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
		});
		e.preventDefault();	
	});

	$(document).on("click", ".allergy", function(e){
		var id = $(".CNR").attr("id");
		req=$.ajax({
			url:'/patient/'+id+'/allergy',
			type: 'GET',
		});
		req.done(function(data){
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
			console.log("allergy");
		});
		e.preventDefault();
	});

	$(document).on("click", ".fam_hist", function(e){
		var id=$(".CNR").attr("id");
		req=$.ajax({
			url:'/patient/'+id+'/familyhistory',
			type: 'GET',
		});
		req.done(function(data){
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
			console.log("famHist");
		});
		e.preventDefault();
	});

	$(document).on("click", ".social_hist", function(e){
		var id=$(".CNR").attr("id")
		req=$.ajax({
			url:'/patient/'+id+'/socialhistory',
			type: 'GET',
		});
		req.done(function(data){
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
			console.log("socialHist");
		});
		e.preventDefault();
	});

	$(document).on("click", ".add_social", function(e){
		console.log("social")
		req=$.ajax({
			url:'/views/creatSocialHist.html',
			type: 'GET',
		});
		req.done(function(data){
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
			console.log("socialHist");
		});
		e.preventDefault();
	});

	$(document).on("click", ".add_gp", function(e){
		
		req=$.ajax({
			url:'/views/addGP.html',
			type: 'GET',
		});
		req.done(function(data){
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
			console.log("socialHist");
		});
		e.preventDefault();
	});
	$(document).on("click", ".view_drugs", function(e){
		
		req=$.ajax({
			url:'/admin/drugs',
			type: 'GET',
		});
		req.done(function(data){
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
			console.log("socialHist");
		});
		e.preventDefault();
	});

	$(document).on("click", ".view_gp", function(e){
		
		req=$.ajax({
			url:'/admin/gp',
			type: 'GET',
		});
		req.done(function(data){
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
			
		});
		e.preventDefault();
	});
	$(document).on("click", "#medlist", function(e){

		req=$.ajax({
			url:'/user/medhistory',
			type: 'GET',
		});
		req.done(function(data){
			document.open()
			document.write(data)
			document.close()
		});
		e.preventDefault();
	});

	$(document).on("click", ".add_famHist", function(e){
		
		req=$.ajax({
			url:'/views/createFamMedHist.html',
			type: 'GET',
		});
		req.done(function(data){
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
	
		});
		e.preventDefault();
	});

	$(document).on("click", ".add_allergy", function(e){
		
		req=$.ajax({
			url:'/user/patients/allergy/new',
			type: 'GET',
		});
		req.done(function(data){
			$('.flex-row').append(data);
			$(".flex-row").scrollLeft(10000);
			console.log("socialHist");
		});
		e.preventDefault();
	});

	//close blade functions

	$(document).on("click", "#plist > .box > .box-header > .box-tools > .exit", function(e){
		$("#plist").remove();
	});

	$(document).on("click", "#profile > .box > .box-header > .box-tools > .exit", function(e){
		$("#profile").remove();
	});

	$(document).on("click", "#CRForm > .box > .box-header > .box-tools > .exit", function(e){
		$("#CRForm").remove();
	});

	$(document).on("click", "#medhistlist > .box > .box-header > .box-tools > .exit", function(e){
		$("#medhistlist").remove();
	});
	$(document).on("click", "#drughist > .box > .box-header > .box-tools > .exit", function(e){
		$("#drughist").remove();
	});
	$(document).on("click", "#socialhist > .box > .box-header > .box-tools > .exit", function(e){
		$("#socialhist").remove();
	});
	$(document).on("click", "#famhist > .box > .box-header > .box-tools > .exit", function(e){
		$("#famhist").remove();
	});
	$(document).on("click", "#radhist > .box > .box-header > .box-tools > .exit", function(e){
		$("#radhist").remove();
	});
	$(document).on("click", "#allergylist > .box > .box-header > .box-tools > .exit", function(e){
		$("#allergylist").remove();
	});
	$(document).on("click", "#crecord > .box > .box-header > .box-tools > .exit", function(e){
		$("#crecord").remove();
	});
	$(document).on("click", "#drugProfile > .box > .box-header > .box-tools > .exit", function(e){
		$("#drugProfile").remove();
	});
	$(document).on("click", "#socialrecord > .box > .box-header > .box-tools > .exit", function(e){
		$("#socialrecord").remove();
	});
	$(document).on("click", "#famreport > .box > .box-header > .box-tools > .exit", function(e){
		$("#famreport").remove();
	});
	$(document).on("click", "#radreport > .box > .box-header > .box-tools > .exit", function(e){
		$("#radreport").remove();
	});
	$(document).on("click", "#allergyrecord > .box > .box-header > .box-tools > .exit", function(e){
		$("#allergyrecord").remove();
	});
	$(document).on("click", "#cSocialHist> .box > .box-header > .box-tools > .exit", function(e){
		$("#cSocialHist").remove();
	});
	$(document).on("click", "#cfamhist> .box > .box-header > .box-tools > .exit", function(e){
		$("#cfamhist").remove();
	});
	$(document).on("click", "#crad> .box > .box-header > .box-tools > .exit", function(e){
		$("#crad").remove();
	});
	$(document).on("click", "#callergy> .box > .box-header > .box-tools > .exit", function(e){
		$("#callergy").remove();
	});
	$(document).on("click", "#aDlist> .box > .box-header > .box-tools > .exit", function(e){
		$("#aDlist").remove();
	});
	$(document).on("click", "#aUlist> .box > .box-header > .box-tools > .exit", function(e){
		$("#aUlist").remove();
	});
	$(document).on("click", "#aMClist> .box > .box-header > .box-tools > .exit", function(e){
		$("#aMClist").remove();
	});
	$(document).on("click", "#aRlist> .box > .box-header > .box-tools > .exit", function(e){
		$("#aRlist").remove();
	});
	$(document).on("click", "#AddUser> .box > .box-header > .box-tools > .exit", function(e){
		$("#AddUser").remove();
	});
	$(document).on("click", "#drugCreate> .box > .box-header > .box-tools > .exit", function(e){
		$("#drugCreate").remove();
	});
	$(document).on("click", "#medicalConditionCreate> .box > .box-header > .box-tools > .exit", function(e){
		$("#medicalConditionCreate").remove();
	});
	$(document).on("click", "#radiologyCreate> .box > .box-header > .box-tools > .exit", function(e){
		$("#radiologyCreate").remove();
	});
	$(document).on("click", "#institutionCreate> .box > .box-header > .box-tools > .exit", function(e){
		$("#institutionCreate").remove();
	});
	$(document).on("click", "#editCRForm> .box > .box-header > .box-tools > .exit", function(e){
		$("#editCRForm").remove();
	});
	$(document).on("click", "#editSocialHist> .box > .box-header > .box-tools > .exit", function(e){
		$("#editSocialHist").remove();
	});
	$(document).on("click", "#editUser> .box > .box-header > .box-tools > .exit", function(e){
		$("#editUser").remove();
	});
	$(document).on("click", "#aplist> .box > .box-header > .box-tools > .exit", function(e){
		$("#aplist").remove();
	});
	$(document).on("click", "#editDrug> .box > .box-header > .box-tools > .exit", function(e){
		$("#editDrug").remove();
	});

	// admin
	$(document).on("click","#admin_patients", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/admin/patients',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#users", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/admin/GP',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});$(document).on("click",".aUTable > tbody > tr", function(e){
		var id =$(this).attr("id");
		req=$.ajax({
			url:'/admin/GP/'+id,
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();

		});
		try{
			e.preventDefault();
		}catch(ReferenceError){

		}

	});
	$(document).on("click","#drugs", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/admin/drug',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#medConditions", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/admin/medConditions',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#radiology", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/admin/radiology',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
	});
		$(document).on("click","#add_patient", function(e){
			req=$.ajax({
			url:'/views/pcreate.html',
			type: 'GET',
			success : function(result){
				document.open();
				document.write(result);
				document.close();
			}
		});
		try{
			e.preventDefault();
		}catch(ReferenceError){

		}
			
	});

	$(document).on("click","#patientsAdd", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/views/aPcreate.html',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#addDrug", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/views/createDrug.html',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#medConditionsAdd", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/views/medicalConCreate.html',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#radiologyAdd", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/views/radiologyCreate.html',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#institutionAdd", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/views/institutionCreate.html',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click",".editCrecord", function(e){
		console.log("clicked");
		id = 1;
		req=$.ajax({
			url:'/views/editCReport.html',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#editsocial", function(e){
		console.log("clicked");
		req=$.ajax({
			url:'/admin/institution/add',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#aUTable > tbody > tr > .edit", function(e){
		console.log("edit");
		req=$.ajax({
			url:'/admin/GP/edit',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#aptable > tbody > tr > .edit", function(e){
		console.log("edit");
		req=$.ajax({
			url:'/admin/GP/edit',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click","#aDTable > tbody > tr > .edit", function(e){
		console.log("edit");
		req=$.ajax({
			url:'/admin/drug/edit',
			type: 'GET',
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			},
		});
		req.done(function(data){
			//console.log("saved");
			//$(".pcreate").remove();
			
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
	$(document).on("click",".editCRSubmit", function(e){
		console.log("edit");
		var id=$(".editCrecord").attr("id")
		req=$.ajax({
			url:'/user/medhistory/'+id,
			type: 'PUT',
			data:{"me":"me"},
			content_type:"application/json",
			success : function(result){
				//$("#pCreate").remove();
				$(".flex-row").append(result);
				$(".flex-row").scrollLeft(10000)
			}
		});
		try{
			e.preventDefault();	
		}catch(ReferenceError){

		}
			
	});
});