#C# code generator (exactly the same as java actually)
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
	
	outfile=open(filename+'.cs','w')
	outfile.write("public class "+ filename+"\n")
	outfile.write("{\n")
	blocklevel= blocklevel+1
	vars=[""]
	commenting=False
	for curtext in text[2:]:

		curtext=curtext.strip('\n ')
		if len(curtext)>0:
			if commenting:
				outfile.write(blocklevel*"\t"+curtext+"\n")
				if len(curtext)>0:
					if(curtext[-1]=='/' and curtext[-2]=='*' ):
						commenting=False
			else:
				#print curtext
				if(curtext[0] =='/' and curtext[1] == '*'):
					commenting=True
					outfile.write(blocklevel*"\t"+curtext+"\n")
					#print 'multiline comment'
				elif (curtext[0] =='/' and curtext[1] == '/'):
					#print 'inline comment'
					outfile.write(blocklevel*"\t"+curtext+"\n")
				
				elif ((curtext)[-1] == ':'):
					#handle access settings
					access= curtext[:-1]
					#print access
				else:
					#handle variable creation
					curtext= curtext.strip(';')
					outfile.write(blocklevel*"\t"+access+" "+curtext+";\n")
					if(access != "public"):
						curtext =curtext.strip(';')
						breakspot= curtext.find('=')
						if breakspot<0:
							vars.append(curtext)
						else:
							vars.append(curtext[:breakspot])
						#print vars
	#end of for loop

	#next generate the get/set functions
	outfile.write("\n"+blocklevel*"\t"+"//get and set functions\n")
	for curvar in vars[1:]:
		newtext= curvar.split()
		#print newtext
		staticity=""
		if newtext[0] == "static":
			staticity="static "
		varname=newtext[-1]
		vartype=newtext[-2]
		#print staticity
		#write set statement
		outfile.write(blocklevel*"\t"+"public "+ staticity+"void " +"set_"+varname+"("+ vartype+" temp)"+"\n"+blocklevel*"\t"+"{\n")
		blocklevel= blocklevel+1
		outfile.write(blocklevel*"\t"+ varname+" = temp;\n")
		blocklevel= blocklevel-1
		outfile.write(blocklevel*"\t"+"}\n")
		
		#write get statement
		outfile.write(blocklevel*"\t"+"public "+ staticity+ vartype +" get_"+ varname +"()"+"\n"+blocklevel*"\t"+"{\n")
		blocklevel= blocklevel+1
		outfile.write(blocklevel*"\t"+"return "+ varname +";\n")
		blocklevel= blocklevel-1
		outfile.write(blocklevel*"\t"+"}\n")


	#close the class
	outfile.write("}\n")
#end of function