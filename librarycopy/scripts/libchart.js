google.load("visualization", "1", {packages:["corechart","table"]});
google.setOnLoadCallback(load);

var levels=[],langs=[],borrows=[];
var options={
          title: 'Library Information',
	  pointSize: 5,
	  vAxis:{title:'Count %', format: '#', viewWindowMode: 'explicit',viewWindow: {min: 0}},
	  hAxis:{title:'Month'},
	  smoothLine: 'true',
	  animation:{
        	duration: 1000,
        	easing: 'out'
      		}
        };

function load(){
	document.getElementById('aggchart').style.display='block';
	document.getElementById('borrowchart').style.display='none';
	charttable('2011-2012','0');
	draw_chart(levels,1);
}

function display(value,type){
	if(value=="agg"){
		document.getElementById('aggchart').style.display='block';
		document.getElementById('borrowchart').style.display='none';
		draw_chart(levels,1);
	}
	else if(value=="borrow"){
		document.getElementById('aggchart').style.display='none';
		document.getElementById('borrowchart').style.display='block';
		draw_chart1(borrows,1);
	}
}

function charttable(year,clas){
	var i,j,k,temp;
	var total=0;
	temp=new Array();
	if(clas==0){
		for(i=1;i<totals.length;i++){
			total=parseInt(total)+parseInt(totals[i][1]);
		}
		document.getElementById("info").innerHTML="Class : All &nbsp;&nbsp;&nbsp; Total Students : "+total;
	}
	else{
		for(i=1;i<totals.length;i++){
			if(totals[i][0]==clas){
				total=parseInt(totals[i][1]);
			}
		}
		document.getElementById("info").innerHTML="Class : "+ clas +" &nbsp;&nbsp;&nbsp; Total Students : "+total;
	}
	if(total==0)
		total=1;
	//alert(total);
	var mon=['Jun','Jul','Aug','Sep','Nov','Dec','Jan','Feb','Mar','Apr','May'];
	levels = new google.visualization.DataTable();
	levels.addColumn('string','month');
	levels.addColumn('number','GREEN');
	levels.addColumn('number','RED');
	levels.addColumn('number','ORRANGE');
	levels.addColumn('number','WHITE');
	levels.addColumn('number','BLUE');
	levels.addColumn('number','YELLOW');
	langs = new google.visualization.DataTable();
	langs.addColumn('string','month');
	langs.addColumn('number','KANNADA');
	langs.addColumn('number','URDU');
	langs.addColumn('number','HINDI');
	langs.addColumn('number','ENGLISH');
	langs.addColumn('number','E/H');
	langs.addColumn('number','E/K');
	langs.addColumn('number','TAMIL');
	langs.addColumn('number','TELUGU');
	borrows = new google.visualization.DataTable();
	borrows.addColumn('string','month');
	borrows.addColumn('number','count');
	for(i=0;i<=mon.length-1;i++){
		temp=[mon[i],0,0,0,0,0,0];
		for(j=1;j<level.length;j++){
			if(level[j][2]==mon[i]){
				if(clas=='0'){
					if(level[j][0]==year){
						temp[1]=parseInt(temp[1])+parseInt(level[j][3]);
						temp[2]=parseInt(temp[2])+parseInt(level[j][4]);
						temp[3]=parseInt(temp[3])+parseInt(level[j][5]);
						temp[4]=parseInt(temp[4])+parseInt(level[j][6]);
						temp[5]=parseInt(temp[5])+parseInt(level[j][7]);
						temp[6]=parseInt(temp[6])+parseInt(level[j][8]);						
					}						
				}
				else{
					if(level[j][0]==year && level[j][1]==clas){
						temp[1]=parseInt(temp[1])+parseInt(level[j][3]);
						temp[2]=parseInt(temp[2])+parseInt(level[j][4]);
						temp[3]=parseInt(temp[3])+parseInt(level[j][5]);
						temp[4]=parseInt(temp[4])+parseInt(level[j][6]);
						temp[5]=parseInt(temp[5])+parseInt(level[j][7]);
						temp[6]=parseInt(temp[6])+parseInt(level[j][8]);						
					}
				}
			}
		}
		for(k=1;k<temp.length;k++){
			temp[k]=parseInt(temp[k])*100/parseInt(total)/4;
		}
		//alert(temp);
		levels.addRow(temp);
		temp=[mon[i],0,0,0,0,0,0,0,0];
		for(j=1;j<lang.length;j++){
			if(lang[j][2]==mon[i]){
				if(clas=='0'){
					if(lang[j][0]==year){
						temp[1]=parseInt(temp[1])+parseInt(lang[j][3]);
						temp[2]=parseInt(temp[2])+parseInt(lang[j][4]);
						temp[3]=parseInt(temp[3])+parseInt(lang[j][5]);
						temp[4]=parseInt(temp[4])+parseInt(lang[j][6]);
						temp[5]=parseInt(temp[5])+parseInt(lang[j][7]);
						temp[6]=parseInt(temp[6])+parseInt(lang[j][8]);						
						temp[7]=parseInt(temp[7])+parseInt(lang[j][9]);
						temp[8]=parseInt(temp[8])+parseInt(lang[j][10]);
					}						
				}
				else{
					if(lang[j][0]==year && lang[j][1]==clas){
						temp[1]=parseInt(temp[1])+parseInt(lang[j][3]);
						temp[2]=parseInt(temp[2])+parseInt(lang[j][4]);
						temp[3]=parseInt(temp[3])+parseInt(lang[j][5]);
						temp[4]=parseInt(temp[4])+parseInt(lang[j][6]);
						temp[5]=parseInt(temp[5])+parseInt(lang[j][7]);
						temp[6]=parseInt(temp[6])+parseInt(lang[j][8]);						
						temp[7]=parseInt(temp[7])+parseInt(lang[j][9]);
						temp[8]=parseInt(temp[8])+parseInt(lang[j][10]);						
					}
				}
			}
		}
		for(k=1;k<temp.length;k++){
			temp[k]=parseInt(temp[k])*100/parseInt(total)/4;
		}
		langs.addRow(temp);
		temp=[mon[i],0];
		for(j=1;j<borrow.length;j++){
			if(borrow[j][2]==mon[i]){
				if(clas=='0'){
					if(borrow[j][0]==year){
						temp[1]=parseInt(temp[1])+parseInt(borrow[j][4]);						
					}						
				}
				else{
					if(borrow[j][0]==year && borrow[j][1]==clas){
						temp[1]=parseInt(temp[1])+parseInt(borrow[j][4]);						
					}
				}
			}
		}
		for(k=1;k<temp.length;k++){
			temp[k]=parseInt(temp[k])*100/parseInt(total)/4;
		}
		borrows.addRow(temp);
	}
}

function draw_chart(data,type){
	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	var table = new google.visualization.Table(document.getElementById('table_div'));
	options['colors']=['Green', 'Red', 'Orange', 'Silver', 'Blue','Yellow','Gray','black'];
	if(type==1)
		chart.draw(data,options);
	else
		table.draw(data);
}

function draw_chart1(data,type){
	var chart = new google.visualization.LineChart(document.getElementById('chart_div1'));
	var table = new google.visualization.Table(document.getElementById('table_div1'));
	if(type==1)
		chart.draw(data,options);
	else
		table.draw(data);
}

function changedata(){
	year=document.getElementById('acyear').value;
	clas=document.getElementById('clas').value;
	charttable(year,clas);
	if(document.getElementById('switch').value=="Switch to Level")
		if(document.getElementById('change').value=="Change to Table View")
			draw_chart(langs,1);
		else
			draw_chart(langs,2);
	else
		if(document.getElementById('change').value=="Change to Table View")
			draw_chart(levels,1);
		else
			draw_chart(levels,2);
	if(document.getElementById('change1').value=="Change to Table View")
		draw_chart1(borrows,1);	
	else
		draw_chart1(borrows,2);
}

function changetype(value){
	if(value=="Switch to Language"){
		document.getElementById('switch').value='Switch to Level';
		if(document.getElementById('change').value=="Change to Table View")
			draw_chart(langs,1);
		else
			draw_chart(langs,2);		
	}
	else{
		document.getElementById('switch').value='Switch to Language';
		if(document.getElementById('change').value=="Change to Table View")
			draw_chart(levels,1);
		else
			draw_chart(levels,2);
	}
}

function changechart(value){
	if(value=="Change to Table View"){
		document.getElementById('change').value="Change to Line Chart";
		document.getElementById('chart_div').style.display="none";
		document.getElementById('table_div').style.display="block";
		if(document.getElementById('switch').value=="Switch to Level")
			draw_chart(langs,2);
		else
			draw_chart(levels,2);
	}
	else{
		
		document.getElementById('change').value="Change to Table View";
		document.getElementById('chart_div').style.display="block";
		document.getElementById('table_div').style.display="none";
		if(document.getElementById('switch').value=="Switch to Level")
			draw_chart(langs,1);
		else
			draw_chart(levels,1);
	}
}

function changeborrowchart(value){
	if(value=="Change to Table View"){
		document.getElementById('change1').value="Change to Line Chart";
		document.getElementById('chart_div1').style.display="none";
		document.getElementById('table_div1').style.display="block";
		draw_chart1(borrows,2);
	}
	else{
		document.getElementById('change1').value="Change to Table View";
		document.getElementById('chart_div1').style.display="block";
		document.getElementById('table_div1').style.display="none";
		draw_chart1(borrows,1);
	}
}
