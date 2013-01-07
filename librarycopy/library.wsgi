import socket
import web
import json

import sys, os,traceback
abspath = os.path.dirname(os.path.abspath(__file__))
#print abspath
if abspath not in sys.path:
	sys.path.append(abspath)
if abspath+'/templates' not in sys.path:
	sys.path.append(abspath+'/templates')

os.chdir(abspath)

render = web.template.render('templates/')
chartrender = web.template.render('charts/')

db=web.database(dbn='postgres',user='postgres',pw='qazwsx',db='klp_institution_master')
db1=web.database(dbn='postgres',user='postgres',pw='qazwsx',db='librarycopy')

urls = (
	'/', 'index',
	'/go','result',
	'/linechart','chart',
	'/chart/','chartoption'
)

values={"dist":'0',"blck":'0',"clst":'0',"schl":'0'}
chartvalues={"type":'lang',"clas":0,"schlid":0,"year":'2011-2012',"chartopt":'agg',"schoolname":""}

sqlstatements={"selectdistrict":"select distinct dist.id,dist.name from vw_tb_schools_boundary as dist, vw_tb_schools_boundary as blck, vw_tb_schools_boundary as clst, vw_institution as inst where clst.parent_id=blck.id and blck.parent_id=dist.id and clst.id=inst.boundary_id and inst.id in (select distinct klp_school_id from lang_agg)",
	"selectblock":"select distinct blck.parent_id,blck.id,blck.name from vw_tb_schools_boundary as dist, vw_tb_schools_boundary as blck, vw_tb_schools_boundary as clst, vw_institution as inst where clst.parent_id=blck.id and blck.parent_id=dist.id and clst.id=inst.boundary_id and inst.id in (select distinct klp_school_id from lang_agg)",
	"selectcluster":"select distinct clst.parent_id,clst.id,clst.name from vw_tb_schools_boundary as dist, vw_tb_schools_boundary as blck,vw_tb_schools_boundary as clst, vw_institution as inst where clst.parent_id=blck.id and blck.parent_id=dist.id and clst.id=inst.boundary_id and inst.id in (select distinct klp_school_id from lang_agg)",
	"selectschool":"select distinct boundary_id,id,name from vw_institution where id in (select distinct klp_school_id from lang_agg)",
	"selectlevelagg":"select month, cast(coalesce(sum(\"GREEN\"),0) as text) as \"GREEN\" , cast(coalesce(sum(\"ORANGE\"),0) as text) as \"ORANGE\" , cast(coalesce(sum(\"WHITE\"),0) as text) as \"WHITE\" , cast(coalesce(sum(\"YELLOW\"),0) as text) as \"YELLOW\" , cast(coalesce(sum(\"NONE\"),0) as text) as \"NONE\" , cast(coalesce(sum(\"RED\"),0) as text) as \"RED\" , cast(coalesce(sum(\"BLUE\"),0) as text) as \"BLUE\"  from ( select month, (case when trim(book_level)='GREEN' then child_count else NULL end) as \"GREEN\", (case when trim(book_level)='ORANGE' then child_count else NULL end) as \"ORANGE\", (case when trim(book_level)='WHITE' then child_count else NULL end) as \"WHITE\", (case when trim(book_level)='YELLOW' then child_count else NULL end) as \"YELLOW\", (case when trim(book_level)='NONE' then child_count else NULL end) as \"NONE\", (case when trim(book_level)='RED' then child_count else NULL end) as \"RED\", (case when trim(book_level)='BLUE' then child_count else NULL end) as \"BLUE\" from (select month,book_level,sum(child_count) as child_count from level_agg where klp_school_id=$schlid and year=$year group by month,book_level) as t) as t group by month",
	"selectlangagg":"select month, cast(coalesce(sum(\"URDU\"),0) as text) as \"URDU\" , cast(coalesce(sum(\"KANNADA\"),0) as text) as \"KANNADA\" , cast(coalesce(sum(\"HINDI\"),0) as text) as \"HINDI\" , cast(coalesce(sum(\"ENGLISH\"),0) as text) as \"ENGLISH\" , cast(coalesce(sum(\"E/H\"),0) as text) as \"E/H\" , cast(coalesce(sum(\"E/K\"),0) as text) as \"E/K\" , cast(coalesce(sum(\"TAMIL\"),0) as text) as \"TAMIL\" , cast(coalesce(sum(\"TELUGU\"),0) as text) as \"TELUGU\"  from ( select month, (case when trim(book_lang)='URDU' then child_count else NULL end) as \"URDU\", (case when trim(book_lang)='KANNADA' then child_count else NULL end) as \"KANNADA\", (case when trim(book_lang)='HINDI' then child_count else NULL end) as \"HINDI\", (case when trim(book_lang)='ENGLISH' then child_count else NULL end) as \"ENGLISH\", (case when trim(book_lang)='E/H' then child_count else NULL end) as \"E/H\", (case when trim(book_lang)='E/K' then child_count else NULL end) as \"E/K\", (case when trim(book_lang)='TAMIL' then child_count else NULL end) as \"TAMIL\", (case when trim(book_lang)='TELUGU' then child_count else NULL end) as \"TELUGU\" from (select month,book_lang,sum(child_count) as child_count from lang_agg where klp_school_id=$schlid and year=$year group by month,book_lang) as t) as t group by month",
	"selectlevelaggclass":"select month, cast(coalesce(sum(\"GREEN\"),0) as text) as \"GREEN\" , cast(coalesce(sum(\"ORANGE\"),0) as text) as \"ORANGE\" , cast(coalesce(sum(\"WHITE\"),0) as text) as \"WHITE\" , cast(coalesce(sum(\"YELLOW\"),0) as text) as \"YELLOW\" , cast(coalesce(sum(\"NONE\"),0) as text) as \"NONE\" , cast(coalesce(sum(\"RED\"),0) as text) as \"RED\" , cast(coalesce(sum(\"BLUE\"),0) as text) as \"BLUE\"  from ( select month, (case when trim(book_level)='GREEN' then child_count else NULL end) as \"GREEN\", (case when trim(book_level)='ORANGE' then child_count else NULL end) as \"ORANGE\", (case when trim(book_level)='WHITE' then child_count else NULL end) as \"WHITE\", (case when trim(book_level)='YELLOW' then child_count else NULL end) as \"YELLOW\", (case when trim(book_level)='NONE' then child_count else NULL end) as \"NONE\", (case when trim(book_level)='RED' then child_count else NULL end) as \"RED\", (case when trim(book_level)='BLUE' then child_count else NULL end) as \"BLUE\" from (select month,book_level,sum(child_count) as child_count from level_agg where klp_school_id=$schlid and year=$year and class=$clas group by month,book_level) as t) as t group by month",
	"selectlangaggclass":"select month, cast(coalesce(sum(\"URDU\"),0) as text) as \"URDU\" , cast(coalesce(sum(\"KANNADA\"),0) as text) as \"KANNADA\" , cast(coalesce(sum(\"HINDI\"),0) as text) as \"HINDI\" , cast(coalesce(sum(\"ENGLISH\"),0) as text) as \"ENGLISH\" , cast(coalesce(sum(\"E/H\"),0) as text) as \"E/H\" , cast(coalesce(sum(\"E/K\"),0) as text) as \"E/K\" , cast(coalesce(sum(\"TAMIL\"),0) as text) as \"TAMIL\" , cast(coalesce(sum(\"TELUGU\"),0) as text) as \"TELUGU\"  from ( select month, (case when trim(book_lang)='URDU' then child_count else NULL end) as \"URDU\", (case when trim(book_lang)='KANNADA' then child_count else NULL end) as \"KANNADA\", (case when trim(book_lang)='HINDI' then child_count else NULL end) as \"HINDI\", (case when trim(book_lang)='ENGLISH' then child_count else NULL end) as \"ENGLISH\", (case when trim(book_lang)='E/H' then child_count else NULL end) as \"E/H\", (case when trim(book_lang)='E/K' then child_count else NULL end) as \"E/K\", (case when trim(book_lang)='TAMIL' then child_count else NULL end) as \"TAMIL\", (case when trim(book_lang)='TELUGU' then child_count else NULL end) as \"TELUGU\" from (select month,book_lang,sum(child_count) as child_count from lang_agg where klp_school_id=$schlid and year=$year and class=$clas group by month,book_lang) as t) as t group by month",
	"getclass":"select distinct(class) as clas from level_agg where klp_school_id=$schl and class is not null order by class",
	"getyear":"select distinct(year) as year from level_agg where klp_school_id=$schl order by year"	
}

dists = [[dist.id,dist.name.title()] for dist in db1.query(sqlstatements["selectdistrict"])]
blcks = [[blck.parent_id,blck.id,blck.name.title()] for blck in db1.query(sqlstatements["selectblock"])]
clsts = [[clst.parent_id,clst.id,clst.name.title()] for clst in db1.query(sqlstatements["selectcluster"])]
schls = [[schl.boundary_id,schl.id,schl.name.title()] for schl in db1.query(sqlstatements["selectschool"])]

class prints:
	def GET(SELF):
		return render.prints()

class index:
	def GET(SELF):
		classes=db1.query(sqlstatements["getclass"],values)
		year=db1.query(sqlstatements["getyear"],values)
		if values["schl"]=='0':
			return render.library(dists,blcks,clsts,schls,values,"",classes,chartvalues,year)
		else :
			return render.library(dists,blcks,clsts,schls,values,"linechart",classes,chartvalues,year)


application = web.application(urls,globals()).wsgifunc()

class chart:
	def GET(self):
            import re
	    os.chdir(abspath+'/templates')
	    if chartvalues["chartopt"]=='agg':
		chartvalues["schlid"]=values["schl"]
		if chartvalues["clas"]=='0':
			chartlevel=db1.query(sqlstatements["selectlevelagg"],chartvalues)
			chartlang=db1.query(sqlstatements["selectlangagg"],chartvalues)
		else:
			chartlevel=db1.query(sqlstatements["selectlevelaggclass"],chartvalues)
			chartlang=db1.query(sqlstatements["selectlangaggclass"],chartvalues)
		months=['Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May']
		resultlevel=[['month','GREEN','RED','ORANGE','WHITE','BLUE','YELLOW']]
		resultlang=[['month','KANNADA','URDU','HINDI','ENGLISH','E/H','E/K','TAMIL','TELUGU']]
		for month in months:
			resultlevel.append([month,0,0,0,0,0,0])
			resultlang.append([month,0,0,0,0,0,0,0,0])
		for row in chartlevel:
			for rows in resultlevel:
				if rows[0]==row.month:
					rows[1]=row.GREEN
					rows[2]=row.RED
					rows[3]=row.ORANGE
					rows[4]=row.WHITE
					rows[5]=row.BLUE
					rows[6]=row.YELLOW
		for row in chartlang:
			for rows in resultlang:
				if rows[0]==row.month:
					rows[1]=row.KANNADA
					rows[2]=row.URDU
					rows[3]=row.HINDI
					rows[4]=row.ENGLISH
					rows[5]=getattr(row,'E/H')
					rows[6]=getattr(row,'E/K')
					rows[7]=row.TAMIL
					rows[8]=row.TELUGU
		return chartrender.linechart(resultlevel,resultlang,chartvalues)
	    else:
		if chartvalues["clas"]=='0':
		    result=db1.query('select getmonth(split_part(issue_date,\'/\',2)) as month,count(klp_child_id) from libentry where flag is not null and klp_school_id=$schlid group by klp_school_id,month',chartvalues)
		else:
	    	    result=db1.query('select getmonth(split_part(issue_date,\'/\',2)) as month,count(klp_child_id) from libentry where flag is not null and klp_school_id=$schlid and class=$clas group by klp_school_id,month',chartvalues)
		months=['Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May']
		resultborrow=[['month','Count']]
		for month in months:
			resultborrow.append([month,0])
		for row in result:
			for rows in resultborrow:
				if rows[0]==row.month:
					rows[1]=row.count
		return chartrender.linechart1(resultborrow,chartvalues)

class chartoption:
	def POST(self):
		inputs=web.input()
		global chartvalues
		chartvalues["basis"]=str(inputs.basis)
		web.seeother('/linechart')

class result:
    def POST(self):
        inputs = web.input()
	global chartvalues
	chartvalues["clas"]=str(inputs.clas)
	try:
		chartvalues["year"]=str(inputs.acyear)
	except:
		chartvalues["year"]='2011-2012'
	chartvalues["chartopt"]=str(inputs.chartopt)
	chartvalues["schoolname"]=str(inputs.schoolname)
	global values		
	values={"dist":inputs.dist,"blck":inputs.blck,"clst":inputs.clst,"schl":inputs.schl}
        raise web.seeother('/')

