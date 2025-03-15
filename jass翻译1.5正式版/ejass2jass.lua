kk={['']=true,[' ']=true,['/']=true,['\n']=true,['+']=true}
function string.gsub2(str,b,b2)
	i1,i2=string.find(str,b)
	if i1==nil then
		return str
	end
	if kk[string.sub(str,i1-1,i1-1)] and kk[string.sub(str,i2+1,i2+1)]then
		return string.gsub(str,b,b2)
	end
	return str
end
function Globals(b,s)
	ENDNUM=ENDNUM+1
	END[ENDNUM]=s
	if global then
		global=false
		table.insert(a,'globals')
		table.insert(a,Global..'endglobals')
		Global=''
	end
end
ejass2jass=nil
function ejass2jass(t)
	starttime=os.clock()
	piece=false;Piece={};piecename=""
f=assert(io.open("./ej.txt","w"))
f:write(t)
f:close()
f=io.open("./ej.txt","r+")--��һ�α�������ȡpiece��Ϊ�˷�ֹpiece���в������﷨����������ܱ�֤����ͨ������������λ�ã����Ա������δ���
	a={}
	for b in f:lines() do
		b=string.gsub2(b,"func","function")
		b=string.gsub2(b,"for","loop")
		b=string.gsub2(b,"int","integer")
		b=string.gsub2(b,"float","real")
		b=string.gsub2(b,"bool","boolean")
		b=string.gsub2(b,"nil","null")
		b=string.gsub2(b,"void","nothing")
		if string.find(b,"endpiece") then--��
			Piece[piecename]=table.concat(Piece[piecename],'\n')
			piece=false
		elseif string.find(b,"piece ") then
			_,_,piecename=string.find(b,"piece%s+(.+)")
			Piece[piecename]={}
			piece=true
		elseif not piece then
			table.insert(a,b)
		end
		if piece and not string.find(b,"piece ") then
			table.insert(Piece[piecename],b)
		end
	end
	a=table.concat(a,"\n")
f:close()
f=assert(io.open("./ej.txt","w+"))
f:write(a)
f:close()
f=assert(io.open("./ej.txt","r"))--�ڶ��α�����insert pieces
a={}
	for b in f:lines() do
		if string.find(b,"insert ") then
			_,_,piecename=string.find(b,"insert%s+([%w_]+)")
			table.insert(a,Piece[piecename])
		else
			table.insert(a,b)
		end
	end
	a=table.concat(a,"\n")
f:close()
f=assert(io.open("./ej.txt","w+"))
f:write(a)
f:close()
f=io.open("./ej.txt","r")
    a={}
    local func=nil
    zinc=false
    END={}
    ENDNUM=0
    InFor=0
    vFor={}
    global=false--��Ϊ�����
    Inglobals=false--ͨ����ȫ�ֱ���
    Global=""
	Func={}--method function ����
	locals={["integer"]=true,["real"]=true,["boolean"]=true,["string"]=true,["sound"]=true,["trackable"]=true,["code"]=true,["texttag"]=true,["image"]=true,["player"]=true}--��������set null �ı�������
	leaklocals={}
	locs=""
	locn=0
	Inloc=false
	struct=false--�Ƿ��ڽṹ���������ڣ�����ȫ���ڽṹ�ڼ���globals
	method=false
	module=false
    interface=false--�Ƿ��ڽӿ��ڣ�����method�ڽӿ�����Ҫend
    for b in f:lines() do--�����α���������ejass
        zs=string.find(b,"//")
        if string.find(b,"//! endzinc") then--�ܿ�zinc
	        zinc=false
    	elseif string.find(b,"//! zinc") then
	    	zinc=true
		elseif zs and not string.find(b,"//!") then--��//�Ҳ���Ԥ����
            b=string.sub(b,0,zs-1)--��ȡ"//"֮ǰ��
        end
        if zinc then--�����zinc
			table.insert(a,b)
        else
        	b=string.gsub(b,"%s*(.+)%s*","%1")
            local dh=string.find(b,"=")
            local len=string.len(b)
            local khz=string.find(b,"%(")--��Ҫֻд��")"��д"("
            local _,_,End=string.find(b,"(.)end")
            if string.find(b,"nothingendfunction") then--��ֹ�滻�ı���
                b=string.gsub(b,"nothing","nothing\n")
            elseif not (func or method) and (string.find(b,"function ") or (string.find(b,"method") and not interface))then--�Ǻ����򷽷����Ҳ��ڽӿڡ������������ڡ�
	            local ej=false
	            local boo=string.find(b,"function ")
	            if boo then--�Ǻ���
                	func=true
					Globals(b,'function')
	            	if not khz then--��ͨ�ĺ�����ʼ
                		table.insert(a,b)
        			else--ej������ʼ
						ej=true
					end
				else--�Ƿ���
					Globals(b,"method")
					method=true
					if not khz or string.find(b,"operator") then--��ͨ�ķ�����ʼ,���������Ż�operator
                		table.insert(a,b)
                	else--ej�ķ���
	                	ej=true
            		end
				end
				if ej then--ej�ķ�������
	           		local ta="";re=""
	           		if string.find(string.sub(b,khz+1,string.find(b,")")-1),"%a") then--����֮��
		            	ta=string.sub(b,khz+1,string.find(b,")")-1)
	            	else
		        		ta='nothing'
		        	end
		        	if string.find(b,">") then--֮�⣬�ж���">"ʱ
			     	    re=string.sub(b,string.find(b,">")+1,len)
		       		else
			    	   	re='nothing'
		        	end
		        	table.insert(a,string.sub(b,1,khz-1).." takes "..ta.." returns "..re)
	        	end
	        	Inloc=true
           	elseif string.find(b,"end") and (End or " ")==" " then--end��
           		local _,_,endstr=string.find(b,"end(%a+)")
           		if interface then
					interface=false
	           	end
           		if not endstr then--��Ϊ�����Ľ�β
		        	if END[ENDNUM]=='function' then
			        	func=false
			        	b=locs..table.concat(Func,'\n')..'\n'..b--loc����+��������+end����
			        	locs=''
			        	Func={}
			        	leaklocals={}
			        	locn=0
			        	vFor={}
		        	elseif END[ENDNUM]=='struct' then
			        	struct=false
			        elseif END[ENDNUM]=='method'then
				        method=false
			     	    b=locs..table.concat(Func,'\n')..'\n'..b
			       	 	locs=''
			      		Func={}
			       		leaklocals={}
			       		locn=0
			        	vFor={}
			        elseif END[ENDNUM]=='module'then
				        module=false
			        elseif END[ENDNUM]=='interface'then
			        	interface=false
					elseif END[ENDNUM]=='globals'then
						Inglobals=false
					end
	        		if func or method then--�ں�����������
		        		if END[ENDNUM]=='for' then
			        		table.insert(Func,'endloop')
							InFor=InFor-1
			        	else
			        		table.insert(Func,b..END[ENDNUM])
						end
					else
						if END[ENDNUM]~=nil then
							b=b..END[ENDNUM]
						else
							b=b..'�����end��β'
						end
	        		end
	        	elseif (func or method) and (endstr=='loop'or endstr=='if'or endstr=='for') then--�����򷽷���
	        		if endstr=='for' then
		        		InFor=InFor-1
		        		table.insert(Func,'endloop')
		        	else
		        		table.insert(Func,b)
					end
				elseif endstr=='function' then--����function��β
					func=false
			        b=locs..table.concat(Func,'\n')..'\n'..b
			        locs=''
			        Func={}
			        leaklocals={}
			        locn=0
			       	vFor={}
				elseif endstr=='struct' then
					struct=false
				elseif endstr=='module' then
					module=false
				elseif endstr=='method' then
					method=false
			        b=locs..table.concat(Func,'\n')..'\n'..b
			        locs=''
			        Func={}
			        leaklocals={}
			        locn=0
			       	vFor={}
				elseif endstr=='interface'then
					interface=false
				elseif endstr=='globals' then--����globals��β
					Inglobals=false
				end
				ENDNUM=ENDNUM-1
			elseif func or method then--������������
	            local loc=nil
	            if string.find(b,"return")
				or string.find(b,"exitwhen")
				or string.find(b,"set")
				or string.find(b,"call") then--��������ų�
				Inloc=false
				elseif string.find(b,'flush locals') then
					loc=true
					Inloc=false
					for _,s in pairs(leaklocals) do
						table.insert(Func,'set '..s..'=null')
					end
					leaklocals={}
				elseif string.find(b,"if")and (not string.find(b,'(%a)if') or string.find(b,'elseif')) then--�����ַ���֮��
					if not string.find(b,"then") then
						b=b..' then'
					end
					Inloc=false
					if not string.find(b,"elseif") then--��elseif
						ENDNUM=ENDNUM+1
						END[ENDNUM]="if"
					end
				elseif string.find(b,'local') then
					locs=locs..b..'\n'
                    local _,_,t,v=string.find(b,"local%s+(%a+)%s+([%w_]+)")--local integer x_2
                    if Inloc then
						loc=true
					elseif dh then
						local _,_,v,f=string.find(b,"([%w_]+)%s*=(.+)")
						b="set "..v..'='..f
					else
						loc=true
					end
                   	if not (locals[t] or string.find(b," array ")) then--����
	                   	locn=locn+1
	                	leaklocals[locn]=v
                    end
				elseif string.find(b,"loop")then
					ENDNUM=ENDNUM+1
					Inloc=false
					local _,_,v,x,y,z=string.find(b,"loop%s+([%w_+-]+)%s*=%s*([%w_+-]+)%s*,%s*([%w_+-]+)(.*)")--for i=1,10,1 do
					if v then
						_,_,z=string.find(z,"([%w_+-]+)%s*")
						if not z then
							z=1
						end
						END[ENDNUM]="for"
						InFor=InFor+1
						b='loop\nset ejv_'..v..'=ejv_'..v..'+'..z..'\nexitwhen ejv_'..v..'>'..y--loop exiwhen v>y v=v+z
						if InFor>1 then
							b='set ejv_'..v..'='..x..'-'..z..'\n'..b
						end
						if vFor[v] then
							b='set ejv_'..v..'='..x..'-'..z..'\n'..b
						else
							locs=locs..'local integer ejv_'..v..'='..x..'-'..z..'\n'
							vFor[InFor]=v
							vFor[v]=true
						end
					else
						END[ENDNUM]="loop"
					end
                elseif khz and not dh then--û��"="����"(",�Զ����call
                    b='call '..b
                    Inloc=false
                elseif string.find((string.sub(b,1,dh or len)),"%a+%s+([%w_]+)")then--Ϊ�����ַ���(�Ⱥ�ǰ)
                    locs=locs.."local "..b..'\n'
                    local _,_,t,v=string.find(b,"(%a+)%s+([%w_]+)")
                    if Inloc then
						loc=true
					elseif dh then
						local _,_,v,f=string.find(b,"([%w_]+)%s*=(.+)")
						b="set "..v..'='..f
					else
						loc=true
					end
                    if not (locals[t] or string.find(b," array ")) then
	                    locn=locn+1
	                    leaklocals[locn]=v
                    end
                elseif dh then--�еȺ�
                    b="set "..b
                    Inloc=false
                elseif string.find(b,"+++")then--�Լ�,++�����⣬���
	                local _,_,v=string.find(b,"(.+)+++")
	                b="set "..v.."="..v.."+1"
	                Inloc=false
                end
                if InFor>0 then
	                for _,v in ipairs(vFor) do
	                	b=string.gsub(b,"([^%w_%.])("..v..")([^%w_%.])","%1ejv_%2%3")
                	end
                end
                if not loc then
                	table.insert(Func,b)
        		end
			elseif string.find(b,"library")then--��
				Globals(b,"library")
				local _,_,IsInit=string.find(b,"library%s+(%a+)")
				if not string.find(b,"initializer") then--init,��һ��library init init init�����
					if IsInit=="init" then
						b=string.gsub(b,"init","libraryname",1)
						b=string.gsub(b,"init","initializer",1)
						b=string.gsub(b,"libraryname","init",1)
					else
						b=string.gsub(b,"init","initializer",1)
					end
				end
			elseif string.find(b,"scope")then--��
				Globals(b,"scope")
			elseif string.find(b,"globals")then--ȫ�ֱ���
				Inglobals=true
				Globals(b,"globals")
			elseif string.find(b,"struct") and not string.find(b,"able")then--�ṹ��
				struct=true
				Globals(b,"struct")
			elseif string.find(b,"module")then--ģ
				module=true
				Globals(b,"module")
			elseif string.find(b,"interface")then--�ӿ�
				interface=true
				Globals(b,"interface")
			elseif string.find((string.sub(b,1,dh or len)),"%a+%s+%a+") and not(struct or interface or module or Inglobals) then--ʡ��globals
				Global=Global..b..'\n'
				global=true
        	end
        	if not (global or func or method) then--���Ǻ�������ȫ�ֱ���������������д
            	table.insert(a,b)
        	end
        end
    end
    a=table.concat(a,'\n')
    a=a.."\n"
f:close()
os.remove("./ej.txt")
return a,os.clock()-starttime
end