#C++ code generator
#Copyright (C) 2007 Jesse Fish
#
#This file is part of code_generator.py
#
#   code_generator.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

def makefile(filename,text):
	blocklevel=0
	access="public"
	
	houtfile=open(filename+'.h','w')
	cppoutfile=open(filename+'.cpp','w')
	houtfile.write("#ifndef "+filename.upper()+"_H"+"\n"+"#define "+filename.upper()+"_H"+"\n")
	houtfile.write("class "+ filename+"\n")
	houtfile.write("{\n")
	blocklevel= blocklevel+1
	vars=[""]
	staticvars=[""]
	commenting=False
	for curtext in text[2:]:
		curtext=curtext.strip('\n ')
		if len(curtext)>0:
			if commenting:
				if len(curtext)>0:
					if(curtext[-1]=='/' and curtext[-2]=='*' ):
						commenting=False
			else:
				if(curtext[0] =='/' and curtext[1] == '*'):
					commenting=True
				elif (curtext[0] =='/' and curtext[1] == '/'):
					pass
				elif ((curtext)[-1] == ':'):
					access=  curtext[:-1]
				else:
					#handle variable creation
					curtext= curtext.strip(';')
					statcheck=curtext.split()
					if(statcheck[0] == "static"):
						curtext =curtext.strip(';')
						staticvars.append(curtext)
					if(access != "public"):
						curtext =curtext.strip(';')
						breakspot= curtext.find('=')
						if breakspot<0:
							vars.append(curtext)
						else:
							vars.append(curtext[:breakspot])
						#print vars
	#end of for loop
	#next generate the get/set function prototypes
	prototypes=[""]
	for curvar in vars[1:]:
		newtext= curvar.split()
		varname=newtext[-1]
		vartype=newtext[-2]
		staticity=""
		if newtext[0] == "static":
			staticity="static "
		prototypes.append(staticity+"void " +"set_"+varname+"("+ vartype+");")
		prototypes.append(staticity+ vartype +" get_"+varname+"();")
	
	#print prototypes

	#write to .h file
	commenting=False
	for curtext in text[2:]:
		curtext=curtext.strip('\n ')
		if len(curtext)>0:
			if commenting:
				houtfile.write(blocklevel*"\t"+curtext+"\n")
				if len(curtext)>0:
					if(curtext[-1]=='/' and curtext[-2]=='*' ):
						commenting=False
			else:
				#print curtext
				if(curtext[0] =='/' and curtext[1] == '*'):
					commenting=True
					houtfile.write(blocklevel*"\t"+curtext+"\n")
					#print 'multiline comment'
				elif (curtext[0] =='/' and curtext[1] == '/'):
					#print 'inline comment'
					houtfile.write(blocklevel*"\t"+curtext+"\n")
				
				elif ((curtext)[-1] == ':'):
					#handle access settings
					if(access=="public"):
						houtfile.write("\n"+blocklevel*"\t"+"//get and set functions\n")
						for temppro in prototypes[1:]:
							houtfile.write(blocklevel*"\t"+temppro+"\n")
					access= curtext[:-1]
					houtfile.write("\n"+blocklevel*"\t"+curtext+"\n")
					#print access
				else:
					#handle variable creation
					curtext= curtext.strip(';')
					curtext =curtext.strip(';')
					breakspot= curtext.find('=')
					if breakspot>=0:
						curtext=curtext[:breakspot]
					houtfile.write(blocklevel*"\t"+curtext+";\n")
	#end of for loop
	
	houtfile.write("};\n#endif\n")

	#generate the cpp file
	cppoutfile.write("#include \""+filename+".h\"\n")
	for curvar in staticvars[1:]:
		curvar=curvar.split()
		#print curvar
		cppoutfile.write(curvar[1]+" "+filename+"::"+curvar[2]+";\n")
	blocklevel=0
	for curvar in vars[1:]:
		newtext= curvar.split()
		#print newtext
		varname=newtext[-1]
		vartype=newtext[-2]
		#write set statement
		cppoutfile.write(blocklevel*"\t"+"void " +filename+"::"+"set_"+varname+"("+ vartype+" temp)"+"\n"+blocklevel*"\t"+"{\n")
		blocklevel= blocklevel+1
		cppoutfile.write(blocklevel*"\t"+ varname+" = temp;\n")
		blocklevel= blocklevel-1
		cppoutfile.write(blocklevel*"\t"+"}\n")
		
		#write get statement
		cppoutfile.write(blocklevel*"\t"+ vartype+" "+filename+"::"+"get_"+ varname +"()"+"\n"+blocklevel*"\t"+"{\n")
		blocklevel= blocklevel+1
		cppoutfile.write(blocklevel*"\t"+"return "+ varname +";\n")
		blocklevel= blocklevel-1
		cppoutfile.write(blocklevel*"\t"+"}\n")


	#close the class

#end of function