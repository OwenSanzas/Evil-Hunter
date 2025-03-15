function analyzer(t)
	starttime=os.clock()
	t=string.lower(t)
	if string.find(t,"unexpected") and string.find(t,"end of lines") then
		t=[[unexpected:end of lines
错误的语句结束(或者说是语句没有正常写完)
解决办法：一般可能是少了括号之类
		]]
	elseif string.find(t,"statement outside of function") then
		t=[[statement outside of function
声明(或动作之类)在函数之外
解决办法：检查你的语法
		]]
	elseif string.find(t,"invalid name") then
		t=[[invalid name
无效的名字
解决办法：修改你的变量名，除逆天变量以外，均不能用中文、标点符号(除"_"以外)，或以数字开头的变量名。
		]]
	elseif string.find(t,"locals are only supported at the top of the function") then
		t=[[locals are only supported at the top of the function
局部变量声明仅支持写在函数的开头
解决办法：把声明放在开头，也就是call set 等之前
		]]
	elseif string.find(t,"undefined type") then
		t=[[undefined type
错误的变量类型
解决办法：检查变量类型
		]]
	elseif string.find(t,"unexpected") and string.find(t,"%)") then
		t=[[unexpected:")"
明显是括号不对应。。
解决办法：检查括号，没问题的话可以看上面的几行有没有错
		]]
	elseif string.find(t,"endblock") then
		t=[[Missing:endblock
少了end类结束或写错了end
解决办法：仔细找吧，估计jasshelper报不到指定行。
		]]
	elseif string.find(t,"unexpected") and string.find(t,"%)") then
		t=[[unexpected:")"
明显是括号不对应。。
解决办法：检查括号，没问题的话可以看上面的几行有没有错
		]]
	elseif string.find(t,"unexpected") and string.find(t,"takes") then
		t=[[unexpected:"takes"
takes有问题
解决办法：检查这个函数，没问题的话可以看上面的几行有没有错
		]]
	elseif string.find(t,"syntax error")and string.find(t,"unexpected")then
		t=[[syntax error:unexpected XXX
语法错误
解决办法：检查你的语法
		]]
	elseif string.find(t,"syntax error") then
		t=[[syntax error
语法错误
解决办法：检查你的语法
		]]
	elseif string.find(t,"cannot convert") then
		t=[[cannot convert X to Y
不能把X转换为Y
解决办法：参数类型、赋值等不准确
		]]
	elseif string.find(t,"too many") then
		t=[[too many arguments given to function
给函数太多了参数
解决办法：看参数数量是否正确
		]]
	elseif string.find(t,"not enough") then
		t=[[not enough arguments given to function
给函数太少了参数
解决办法：看参数数量是否正确
		]]
	elseif string.find(t,"function redeclared") then
		t=[[function redeclared
函数重名
解决办法：改函数名，有时候也可能是YD的本身错误，重启YD试试吧。
		]]
	elseif string.find(t,"undeclared function") then
		t=[[undeclared function
没有这个函数
解决办法：没有这个函数，可能是你智能注入未打开或不正常。
		]]
	elseif string.find(t,"indentifier redeclared") then
		t=[[indentifier redeclared
标志符重名（可能是变量名）
解决办法：改吧。。
		]]
	elseif string.find(t,"already defined as variable") then
		t=[[XX already defined as variable
XX已经被当作变量定义了
解决办法：改吧。。
		]]
	elseif string.find(t,"variable") and string.find(t,"used without having been initializered") then
		t=[[variable XX used without having been initializered
XX没有被赋值就使用了（并且后面其他动作会失效）
解决办法：赋值
		]]
	elseif string.find(t,"hit opcode limit") then
		t=[[hit opcode limit
		执行的代码超过了限制
解决办法：查看是否有死循环的发生，或者可能是初始化执行的代码过多(合并触发或休眠或动态注册都可以解决)。
这里的非真正的死循环，真的死循环会崩魔兽，这个死循环是指循环动作类的循环
		]]
	else
		t=[[没有找到你的错误，请注意你是否打错了字，或者遇到了很稀有的错误。。
现在只支持比较常见的jasshelper报错及YD的CMD(黑窗)报错。魔兽崩溃请用crash文件分析。
		]]
	end
	return t,os.clock()-starttime
end