require "wx"
require "trans"
--require "yj"
--require "gjl"
frame = nil--����GUI
fileMenu=nil--�˵�
statusBar=nil--״̬��
require "jass2chinese"
require "ejass2jass"
require "analyzer"
func={[99]=ejass2jass,[98]=jass2chinese,[97]=analyzer}
function PrintText(event)
	local id=event:GetId()
	text=Text1:GetValue()
	text,t=func[id](text)
	frame:SetStatusText("��ʱ"..string.format("%3.5f",t).."��",2)
	Text2:SetValue(text)
end
function Button()
	button1=wx.wxButton(frame,99,"ejת��j",wx.wxPoint(300,0))--wx.wxPoint(50,50)����
	button2=wx.wxButton(frame,98,"jת������",wx.wxPoint(300,0))
	button3=wx.wxButton(frame,97,"�������",wx.wxPoint(300,0))
	sizer=wx.wxBoxSizer(wx.wxHORIZONTAL)--wxVERTICAL��ֱ��wxHORIZONTALˮƽ
	sizer2=wx.wxBoxSizer(wx.wxVERTICAL)
	sizer:Add(Text1,4,wx.wxEXPAND,6)
	sizer2:Add(button1,1,wx.wxEXPAND,3)--wxEXPAND�ɱ����죬����2Ϊ��
	sizer2:Add(button2,1,wx.wxEXPAND,3)
	sizer2:Add(button3,1,wx.wxEXPAND,3)
	sizer:Add(sizer2,1,wx.wxEXPAND,6)
	sizer:Add(Text2,4,wx.wxEXPAND,6)
	--sizer:SetSizeHints(frame)--����sizer�Զ����ó���ߴ硣
	frame:SetSizer(sizer)
	--button2:Move(50,50)�ƶ�����
	frame:Connect(99,--����¼���
	wx.wxEVT_COMMAND_BUTTON_CLICKED,function(event)PrintText(event)end)
	frame:Connect(98,
	wx.wxEVT_COMMAND_BUTTON_CLICKED,function(event)PrintText(event)end)
	frame:Connect(97,
	wx.wxEVT_COMMAND_BUTTON_CLICKED,function(event)PrintText(event)end)
end
function menu()
	fileMenu=wx.wxMenu()--�˵�����

	local loginico = wx.wxBitmap("./test.ico", wx.wxBITMAP_TYPE_ICO)
	--����һ��λͼ������Ϊ�˵���ͼ��
	local m = wx.wxMenuItem(fileMenu, 1005, "��(&O)\tCtrl+O", "���ļ�")
	m:SetBitmap(loginico)--����λͼͼ��
	fileMenu:Append(m)

	fileMenu:AppendSeparator()--Ϊ�˵�������ӷָ��ߡ�

	fileMenu:Append(wx.wxID_EXIT,"�˳�(&X)\tCtrl+Q","�˳�����")--������wx.wxID_EXIT�ǲ˵�ѡ���ID
	local menuBar=wx.wxMenuBar()--�˵�������
	menuBar:Append(fileMenu,"�ļ�(&F)")--�˵�����Ӳ˵�
	frame:SetMenuBar(menuBar)
	frame:Connect(1005,wx.wxEVT_COMMAND_MENU_SELECTED,
	function(event)
		path=wx.wxFileSelector("���ı��ļ�","./","","","�ı��ļ� (*.txt)|*.txt|�����ļ� (*.*)|*.*")
		if path=="" then
			return
		end
		file=io.open(path,"r")
		local text=file:read("*a")
		Text1:SetValue(text)
	end)
	frame:Connect(wx.wxID_EXIT,wx.wxEVT_COMMAND_MENU_SELECTED,function (event) frame:Close(true) end)
	--�˵����¼���frame:Close(true)�˳�
end
function main()
    frame = wx.wxFrame( wx.NULL, wx.wxID_ANY, "jass����",
     	wx.wxDefaultPosition, wx.wxSize(600, 400),
       	wx.wxDEFAULT_FRAME_STYLE )--��ʽ+���� wx.wxSTAY_ON_TOP

	Text1=wx.wxTextCtrl(frame,50," ",--�ı���
        	wx.wxDefaultPosition,wx.wxSize(265,315),
            wx.wxTE_MULTILINE)
    Text2=wx.wxTextCtrl(frame,51," ",--�ı���
        	wx.wxPoint(320,0),wx.wxSize(265,315),
            wx.wxTE_MULTILINE)
	menu()--�˵�

	statusBar=frame:CreateStatusBar(3)--״̬����
	frame:SetStatusText("ej��j�໥ת��")
	frame:SetStatusText("����Q:�Ѿ�����",1)
	frame:SetStatusText("��ʱ",2)
    frame:SetIcon(wx.wxIcon("./test.ico",wx.wxBITMAP_TYPE_ICO))--����ͼ��

	--local optionMenu = wx.wxMenu()--��ѡ�˵���
	--optionMenu:AppendCheckItem( 1005, "�����ڶ���", "���ִ��������ϲ�")
	--optionMenu:Check(1005, true)--ѡ�и�ѡ�˵���
	
	--local menuBar = wx.wxMenuBar()--�˵�������
	--menuBar:Append(optionMenu, "ѡ��(&O)")
	
	--toolMenu:Enable(1006, false)--ʹ�˵�����Ч
	
	--yj()--�Ҽ�����
	--gjl()--��ӹ�����
	Button()
	frame:Connect(1004, wx.wxEVT_COMMAND_MENU_SELECTED,
		function (event)
			if event:IsChecked() then
				frame:SetWindowStyle( wx.wxDEFAULT_FRAME_STYLE + wx.wxSTAY_ON_TOP )
			else
				frame:SetWindowStyle( wx.wxDEFAULT_FRAME_STYLE )
			end            
		end)
	
	--frame:Maximize(true)--���
    frame:Show(true)
    taskbarIcon = wx.wxTaskBarIcon()--������ͼ�����
	taskbarIcon:SetIcon(wx.wxIcon("./test.ico",wx.wxBITMAP_TYPE_ICO), "J2EJ")--������ͼ��
	if taskbarIcon then
      taskbarIcon:delete()--ɾ��ͼ��
	end
end
main()
wx.wxGetApp():MainLoop()--����ѭ��״̬
