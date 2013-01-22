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

db=web.database(dbn='postgres',user='postgres',pw='qazwsx',db='librarycopy')

sqlstatements={"selectdistrict":"select distinct dist.id,dist.name from vw_tb_schools_boundary as dist, vw_tb_schools_boundary as blck, vw_tb_schools_boundary as clst, vw_institution as inst where clst.parent_id=blck.id and blck.parent_id=dist.id and clst.id=inst.boundary_id and inst.id in (select distinct klp_school_id from lang_agg)",
	"selectblock":"select distinct blck.parent_id,blck.id,blck.name from vw_tb_schools_boundary as dist, vw_tb_schools_boundary as blck, vw_tb_schools_boundary as clst, vw_institution as inst where clst.parent_id=blck.id and blck.parent_id=dist.id and clst.id=inst.boundary_id and inst.id in (select distinct klp_school_id from lang_agg)",
	"selectcluster":"select distinct clst.parent_id,clst.id,clst.name from vw_tb_schools_boundary as dist, vw_tb_schools_boundary as blck,vw_tb_schools_boundary as clst, vw_institution as inst where clst.parent_id=blck.id and blck.parent_id=dist.id and clst.id=inst.boundary_id and inst.id in (select distinct klp_school_id from lang_agg)",
	"selectschool":"select distinct boundary_id,id,name from vw_institution where id in (select distinct klp_school_id from lang_agg)",
	"selectlevelagg":"select year,class as clas,month, cast(coalesce(sum(\"GREEN\"),0) as text) as \"GREEN\" , cast(coalesce(sum(\"ORANGE\"),0) as text) as \"ORANGE\" , cast(coalesce(sum(\"WHITE\"),0) as text) as \"WHITE\" , cast(coalesce(sum(\"YELLOW\"),0) as text) as \"YELLOW\" , cast(coalesce(sum(\"NONE\"),0) as text) as \"NONE\" , cast(coalesce(sum(\"RED\"),0) as text) as \"RED\" , cast(coalesce(sum(\"BLUE\"),0) as text) as \"BLUE\" from ( select year,class,month, (case when trim(book_level)='GREEN' then child_count else NULL end) as \"GREEN\", (case when trim(book_level)='ORANGE' then child_count else NULL end) as \"ORANGE\", (case when trim(book_level)='WHITE' then child_count else NULL end) as \"WHITE\", (case when trim(book_level)='YELLOW' then child_count else NULL end) as \"YELLOW\", (case when trim(book_level)='NONE' then child_count else NULL end) as \"NONE\", (case when trim(book_level)='RED' then child_count else NULL end) as \"RED\", (case when trim(book_level)='BLUE' then child_count else NULL end) as \"BLUE\" from (select year,class,month,book_level,sum(child_count) as child_count from level_agg where klp_school_id=$schlid group by month,book_level,class,year) as t) as t group by month,class,year",
	"selectlangagg":"select year,class as clas,month, cast(coalesce(sum(\"URDU\"),0) as text) as \"URDU\" , cast(coalesce(sum(\"KANNADA\"),0) as text) as \"KANNADA\" , cast(coalesce(sum(\"HINDI\"),0) as text) as \"HINDI\" , cast(coalesce(sum(\"ENGLISH\"),0) as text) as \"ENGLISH\" , cast(coalesce(sum(\"E/H\"),0) as text) as \"E/H\" , cast(coalesce(sum(\"E/K\"),0) as text) as \"E/K\" , cast(coalesce(sum(\"TAMIL\"),0) as text) as \"TAMIL\" , cast(coalesce(sum(\"TELUGU\"),0) as text) as \"TELUGU\" from ( select year,class,month, (case when trim(book_lang)='URDU' then child_count else NULL end) as \"URDU\", (case when trim(book_lang)='KANNADA' then child_count else NULL end) as \"KANNADA\", (case when trim(book_lang)='HINDI' then child_count else NULL end) as \"HINDI\", (case when trim(book_lang)='ENGLISH' then child_count else NULL end) as \"ENGLISH\", (case when trim(book_lang)='E/H' then child_count else NULL end) as \"E/H\", (case when trim(book_lang)='E/K' then child_count else NULL end) as \"E/K\", (case when trim(book_lang)='TAMIL' then child_count else NULL end) as \"TAMIL\", (case when trim(book_lang)='TELUGU' then child_count else NULL end) as \"TELUGU\" from (select year,class,month,book_lang,sum(child_count) as child_count from lang_agg where klp_school_id=$schlid group by month,book_lang,class,year) as t) as t group by month,class,year",
	"selectborrow":"select academic_year,class as clas,getmonth(split_part(issue_date,\'/\',2)) as month,school_name,count(klp_child_id) from libentry where flag is not null and klp_school_id=$schlid and flag is not null group by klp_school_id,month,academic_year,class,school_name",
	"selectclass":"select distinct class as clas from level_agg where class is not null and klp_school_id=$schlid order by class",
	"selectyear":"select distinct year from level_agg where class is not null and klp_school_id=$schlid",
	"selecttotalstudents":"select class as clas,count from vw_totalstudents where klp_school_id=$schlid"
}

dists = [[dist.id,dist.name.title()] for dist in db.query(sqlstatements["selectdistrict"])]
blcks = [[blck.parent_id,blck.id,blck.name.title()] for blck in db.query(sqlstatements["selectblock"])]
clsts = [[clst.parent_id,clst.id,clst.name.title()] for clst in db.query(sqlstatements["selectcluster"])]
schls = [[schl.boundary_id,schl.id,schl.name.title()] for schl in db.query(sqlstatements["selectschool"])]

urls = (
	'/', 'index',
	'/selection','top',
	'/libchart/(.*)','libchart',
	'/go','result',
	'/linechart','chart',
	'/chart/','chartoption'
)


class index:
	def GET(SELF):
		return render.main()

class top:
	def GET(SELF):
		return render.topframe(dists,blcks,clsts,schls)

class libchart:
	def GET(SELF,schlid):
		resultlevel=[['year','clas','month','GREEN','ORANGE','WHITE','YELLOW','NONE','RED','BLUE']]
		resultlang=[['year','clas','month','URDU','KANNADA','HINDI','ENGLISH','E/H','E/K','TAMIL','TELUGU']]
		resultborrow=[['academic_year','clas','month','school_name','count']]
		classtotal=[['clas','total']]
		clas=[]
		year=[]
		for row in db.query(sqlstatements["selectlevelagg"],{"schlid":schlid}):
			resultlevel.append([row.year,row.clas,row.month,row.GREEN,row.RED,row.ORANGE,row.WHITE,row.BLUE,row.YELLOW])
		for row in db.query(sqlstatements["selectlangagg"],{"schlid":schlid}):
			resultlang.append([row.year,row.clas,row.month,row.KANNADA,row.URDU,row.HINDI,row.ENGLISH,getattr(row,'E/H'),getattr(row,'E/K'),row.TAMIL,row.TELUGU])
		for row in db.query(sqlstatements["selectborrow"],{"schlid":schlid}):
			resultborrow.append([row.academic_year,row.clas,row.month,row.school_name,row.count])
		for row in db.query(sqlstatements["selectclass"],{"schlid":schlid}):
			clas.append(row.clas)
		for row in db.query(sqlstatements["selectyear"],{"schlid":schlid}):
			year.append(row.year)
		for row in db.query(sqlstatements["selecttotalstudents"],{"schlid":schlid}):
			classtotal.append(row.clas,row.count)		
		return render.libchart(schlid,resultlevel,resultlang,resultborrow,clas,year,classtotal)


application = web.application(urls,globals()).wsgifunc()

