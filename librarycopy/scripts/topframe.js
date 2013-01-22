function filldropdown(value,type){
	var optionlist=new Array();
	var selectbox=document.getElementById(type);
	selectbox.options.length=1;
	if(type=='blck'){
		document.getElementById('clst').options.length=1;
		document.getElementById('schl').options.length=1;
		optionlist=block;
	}
	else if(type=='clst'){
		document.getElementById('schl').options.length=1;
		optionlist=cluster;
	}
	else if(type=='schl'){
		optionlist=school;
	}
	for(i=0,j=0;i<=optionlist.length-1;i++){
                if(optionlist[i][0]==value){
			selectbox.options[j+1]=new Option(optionlist[i][2],optionlist[i][1]);
			j=j+1
		}
	}
}	

function callchart(value){
	parent.charts.location.href="libchart/"+value;
}
