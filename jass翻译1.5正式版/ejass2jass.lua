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
f=io.open("./ej.txt","r+")--第一次遍历。获取piece，为了防止piece里有不符合语法的情况并且能保证编译通过。还是任意位置，所以遍历三次代码
	a={}
	for b in f:lines() do
		b=string.gsub2(b,"func","function")
		b=string.gsub2(b,"for","loop")
		b=string.gsub2(b,"int","integer")
		b=string.gsub2(b,"float","real")
		b=string.gsub2(b,"bool","boolean")
		b=string.gsub2(b,"nil","null")
		b=string.gsub2(b,"void","nothing")
		if string.find(b,"endpiece") then--块
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
f=assert(io.open("./ej.txt","r"))--第二次遍历，insert pieces
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
    global=false--仅为特殊的
    Inglobals=false--通常的全局变量
    Global=""
	Func={}--method function 公用
	locals={["integer"]=true,["real"]=true,["boolean"]=true,["string"]=true,["sound"]=true,["trackable"]=true,["code"]=true,["texttag"]=true,["image"]=true,["player"]=true}--常见不必set null 的变量类型
	leaklocals={}
	locs=""
	locn=0
	Inloc=false
	struct=false--是否在结构、方法等内，避免全局在结构内加上globals
	method=false
	module=false
    interface=false--是否在接口内，避免method在接口内需要end
    for b in f:lines() do--第三次遍历，编译ejass
        zs=string.find(b,"//")
        if string.find(b,"//! endzinc") then--避开zinc
	        zinc=false
    	elseif string.find(b,"//! zinc") then
	    	zinc=true
		elseif zs and not string.find(b,"//!") then--有//且不是预处理
            b=string.sub(b,0,zs-1)--截取"//"之前的
        end
        if zinc then--如果是zinc
			table.insert(a,b)
        else
        	b=string.gsub(b,"%s*(.+)%s*","%1")
            local dh=string.find(b,"=")
            local len=string.len(b)
            local khz=string.find(b,"%(")--不要只写了")"不写"("
            local _,_,End=string.find(b,"(.)end")
            if string.find(b,"nothingendfunction") then--防止替换的报错
                b=string.gsub(b,"nothing","nothing\n")
            elseif not (func or method) and (string.find(b,"function ") or (string.find(b,"method") and not interface))then--是函数或方法，且不在接口、方法、函数内。
	            local ej=false
	            local boo=string.find(b,"function ")
	            if boo then--是函数
                	func=true
					Globals(b,'function')
	            	if not khz then--普通的函数开始
                		table.insert(a,b)
        			else--ej函数开始
						ej=true
					end
				else--是方法
					Globals(b,"method")
					method=true
					if not khz or string.find(b,"operator") then--普通的方法开始,不含左括号或含operator
                		table.insert(a,b)
                	else--ej的方法
	                	ej=true
            		end
				end
				if ej then--ej的方法或函数
	           		local ta="";re=""
	           		if string.find(string.sub(b,khz+1,string.find(b,")")-1),"%a") then--括号之间
		            	ta=string.sub(b,khz+1,string.find(b,")")-1)
	            	else
		        		ta='nothing'
		        	end
		        	if string.find(b,">") then--之外，判断无">"时
			     	    re=string.sub(b,string.find(b,">")+1,len)
		       		else
			    	   	re='nothing'
		        	end
		        	table.insert(a,string.sub(b,1,khz-1).." takes "..ta.." returns "..re)
	        	end
	        	Inloc=true
           	elseif string.find(b,"end") and (End or " ")==" " then--end类
           		local _,_,endstr=string.find(b,"end(%a+)")
           		if interface then
					interface=false
	           	end
           		if not endstr then--不为正常的结尾
		        	if END[ENDNUM]=='function' then
			        	func=false
			        	b=locs..table.concat(Func,'\n')..'\n'..b--loc部分+其他部分+end部分
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
	        		if func or method then--在函数、方法内
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
							b=b..'错误的end结尾'
						end
	        		end
	        	elseif (func or method) and (endstr=='loop'or endstr=='if'or endstr=='for') then--函数或方法内
	        		if endstr=='for' then
		        		InFor=InFor-1
		        		table.insert(Func,'endloop')
		        	else
		        		table.insert(Func,b)
					end
				elseif endstr=='function' then--正常function结尾
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
				elseif endstr=='globals' then--正常globals结尾
					Inglobals=false
				end
				ENDNUM=ENDNUM-1
			elseif func or method then--函数、方法内
	            local loc=nil
	            if string.find(b,"return")
				or string.find(b,"exitwhen")
				or string.find(b,"set")
				or string.find(b,"call") then--正常语句排除
				Inloc=false
				elseif string.find(b,'flush locals') then
					loc=true
					Inloc=false
					for _,s in pairs(leaklocals) do
						table.insert(Func,'set '..s..'=null')
					end
					leaklocals={}
				elseif string.find(b,"if")and (not string.find(b,'(%a)if') or string.find(b,'elseif')) then--避免字符串之类
					if not string.find(b,"then") then
						b=b..' then'
					end
					Inloc=false
					if not string.find(b,"elseif") then--非elseif
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
                   	if not (locals[t] or string.find(b," array ")) then--数组
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
                elseif khz and not dh then--没有"="且有"(",自动添加call
                    b='call '..b
                    Inloc=false
                elseif string.find((string.sub(b,1,dh or len)),"%a+%s+([%w_]+)")then--为两个字符串(等号前)
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
                elseif dh then--有等号
                    b="set "..b
                    Inloc=false
                elseif string.find(b,"+++")then--自加,++有问题，无语。
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
			elseif string.find(b,"library")then--库
				Globals(b,"library")
				local _,_,IsInit=string.find(b,"library%s+(%a+)")
				if not string.find(b,"initializer") then--init,万一有library init init init的情况
					if IsInit=="init" then
						b=string.gsub(b,"init","libraryname",1)
						b=string.gsub(b,"init","initializer",1)
						b=string.gsub(b,"libraryname","init",1)
					else
						b=string.gsub(b,"init","initializer",1)
					end
				end
			elseif string.find(b,"scope")then--域
				Globals(b,"scope")
			elseif string.find(b,"globals")then--全局变量
				Inglobals=true
				Globals(b,"globals")
			elseif string.find(b,"struct") and not string.find(b,"able")then--结构体
				struct=true
				Globals(b,"struct")
			elseif string.find(b,"module")then--模
				module=true
				Globals(b,"module")
			elseif string.find(b,"interface")then--接口
				interface=true
				Globals(b,"interface")
			elseif string.find((string.sub(b,1,dh or len)),"%a+%s+%a+") and not(struct or interface or module or Inglobals) then--省略globals
				Global=Global..b..'\n'
				global=true
        	end
        	if not (global or func or method) then--若非函数或是全局变量、方法则不立即写
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