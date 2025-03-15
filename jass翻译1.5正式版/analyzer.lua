function analyzer(t)
	starttime=os.clock()
	t=string.lower(t)
	if string.find(t,"unexpected") and string.find(t,"end of lines") then
		t=[[unexpected:end of lines
�����������(����˵�����û������д��)
����취��һ���������������֮��
		]]
	elseif string.find(t,"statement outside of function") then
		t=[[statement outside of function
����(����֮��)�ں���֮��
����취���������﷨
		]]
	elseif string.find(t,"invalid name") then
		t=[[invalid name
��Ч������
����취���޸���ı�������������������⣬�����������ġ�������(��"_"����)���������ֿ�ͷ�ı�������
		]]
	elseif string.find(t,"locals are only supported at the top of the function") then
		t=[[locals are only supported at the top of the function
�ֲ�����������֧��д�ں����Ŀ�ͷ
����취�����������ڿ�ͷ��Ҳ����call set ��֮ǰ
		]]
	elseif string.find(t,"undefined type") then
		t=[[undefined type
����ı�������
����취������������
		]]
	elseif string.find(t,"unexpected") and string.find(t,"%)") then
		t=[[unexpected:")"
���������Ų���Ӧ����
����취��������ţ�û����Ļ����Կ�����ļ�����û�д�
		]]
	elseif string.find(t,"endblock") then
		t=[[Missing:endblock
����end�������д����end
����취����ϸ�Ұɣ�����jasshelper������ָ���С�
		]]
	elseif string.find(t,"unexpected") and string.find(t,"%)") then
		t=[[unexpected:")"
���������Ų���Ӧ����
����취��������ţ�û����Ļ����Կ�����ļ�����û�д�
		]]
	elseif string.find(t,"unexpected") and string.find(t,"takes") then
		t=[[unexpected:"takes"
takes������
����취��������������û����Ļ����Կ�����ļ�����û�д�
		]]
	elseif string.find(t,"syntax error")and string.find(t,"unexpected")then
		t=[[syntax error:unexpected XXX
�﷨����
����취���������﷨
		]]
	elseif string.find(t,"syntax error") then
		t=[[syntax error
�﷨����
����취���������﷨
		]]
	elseif string.find(t,"cannot convert") then
		t=[[cannot convert X to Y
���ܰ�Xת��ΪY
����취���������͡���ֵ�Ȳ�׼ȷ
		]]
	elseif string.find(t,"too many") then
		t=[[too many arguments given to function
������̫���˲���
����취�������������Ƿ���ȷ
		]]
	elseif string.find(t,"not enough") then
		t=[[not enough arguments given to function
������̫���˲���
����취�������������Ƿ���ȷ
		]]
	elseif string.find(t,"function redeclared") then
		t=[[function redeclared
��������
����취���ĺ���������ʱ��Ҳ������YD�ı����������YD���԰ɡ�
		]]
	elseif string.find(t,"undeclared function") then
		t=[[undeclared function
û���������
����취��û�����������������������ע��δ�򿪻�������
		]]
	elseif string.find(t,"indentifier redeclared") then
		t=[[indentifier redeclared
��־�������������Ǳ�������
����취���İɡ���
		]]
	elseif string.find(t,"already defined as variable") then
		t=[[XX already defined as variable
XX�Ѿ�����������������
����취���İɡ���
		]]
	elseif string.find(t,"variable") and string.find(t,"used without having been initializered") then
		t=[[variable XX used without having been initializered
XXû�б���ֵ��ʹ���ˣ����Һ�������������ʧЧ��
����취����ֵ
		]]
	elseif string.find(t,"hit opcode limit") then
		t=[[hit opcode limit
		ִ�еĴ��볬��������
����취���鿴�Ƿ�����ѭ���ķ��������߿����ǳ�ʼ��ִ�еĴ������(�ϲ����������߻�̬ע�ᶼ���Խ��)��
����ķ���������ѭ���������ѭ�����ħ�ޣ������ѭ����ָѭ���������ѭ��
		]]
	else
		t=[[û���ҵ���Ĵ�����ע�����Ƿ������֣����������˺�ϡ�еĴ��󡣡�
����ֻ֧�ֱȽϳ�����jasshelper����YD��CMD(�ڴ�)����ħ�ޱ�������crash�ļ�������
		]]
	end
	return t,os.clock()-starttime
end