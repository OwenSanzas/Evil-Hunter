require "wx"
require "trans"
--require "yj"
--require "gjl"
frame = nil--主体GUI
fileMenu=nil--菜单
statusBar=nil--状态栏
require "jass2chinese"
require "ejass2jass"
require "analyzer"
func={[99]=ejass2jass,[98]=jass2chinese,[97]=analyzer}
function PrintText(event)
	local id=event:GetId()
	text=Text1:GetValue()
	text,t=func[id](text)
	frame:SetStatusText("用时"..string.format("%3.5f",t).."秒",2)
	Text2:SetValue(text)
end
function Button()
	button1=wx.wxButton(frame,99,"ej转换j",wx.wxPoint(300,0))--wx.wxPoint(50,50)坐标
	button2=wx.wxButton(frame,98,"j转换中文",wx.wxPoint(300,0))
	button3=wx.wxButton(frame,97,"报错分析",wx.wxPoint(300,0))
	sizer=wx.wxBoxSizer(wx.wxHORIZONTAL)--wxVERTICAL垂直、wxHORIZONTAL水平
	sizer2=wx.wxBoxSizer(wx.wxVERTICAL)
	sizer:Add(Text1,4,wx.wxEXPAND,6)
	sizer2:Add(button1,1,wx.wxEXPAND,3)--wxEXPAND可被拉伸，参数2为高
	sizer2:Add(button2,1,wx.wxEXPAND,3)
	sizer2:Add(button3,1,wx.wxEXPAND,3)
	sizer:Add(sizer2,1,wx.wxEXPAND,6)
	sizer:Add(Text2,4,wx.wxEXPAND,6)
	--sizer:SetSizeHints(frame)--根据sizer自动设置程序尺寸。
	frame:SetSizer(sizer)
	--button2:Move(50,50)移动坐标
	frame:Connect(99,--添加事件。
	wx.wxEVT_COMMAND_BUTTON_CLICKED,function(event)PrintText(event)end)
	frame:Connect(98,
	wx.wxEVT_COMMAND_BUTTON_CLICKED,function(event)PrintText(event)end)
	frame:Connect(97,
	wx.wxEVT_COMMAND_BUTTON_CLICKED,function(event)PrintText(event)end)
end
function menu()
	fileMenu=wx.wxMenu()--菜单对象

	local loginico = wx.wxBitmap("./test.ico", wx.wxBITMAP_TYPE_ICO)
	--生成一个位图对象作为菜单的图标
	local m = wx.wxMenuItem(fileMenu, 1005, "打开(&O)\tCtrl+O", "打开文件")
	m:SetBitmap(loginico)--设置位图图标
	fileMenu:Append(m)

	fileMenu:AppendSeparator()--为菜单对象添加分割线。

	fileMenu:Append(wx.wxID_EXIT,"退出(&X)\tCtrl+Q","退出程序")--在这里wx.wxID_EXIT是菜单选项的ID
	local menuBar=wx.wxMenuBar()--菜单栏对象
	menuBar:Append(fileMenu,"文件(&F)")--菜单栏添加菜单
	frame:SetMenuBar(menuBar)
	frame:Connect(1005,wx.wxEVT_COMMAND_MENU_SELECTED,
	function(event)
		path=wx.wxFileSelector("打开文本文件","./","","","文本文件 (*.txt)|*.txt|所有文件 (*.*)|*.*")
		if path=="" then
			return
		end
		file=io.open(path,"r")
		local text=file:read("*a")
		Text1:SetValue(text)
	end)
	frame:Connect(wx.wxID_EXIT,wx.wxEVT_COMMAND_MENU_SELECTED,function (event) frame:Close(true) end)
	--菜单绑定事件，frame:Close(true)退出
end
function main()
    frame = wx.wxFrame( wx.NULL, wx.wxID_ANY, "jass翻译",
     	wx.wxDefaultPosition, wx.wxSize(600, 400),
       	wx.wxDEFAULT_FRAME_STYLE )--样式+顶置 wx.wxSTAY_ON_TOP

	Text1=wx.wxTextCtrl(frame,50," ",--文本栏
        	wx.wxDefaultPosition,wx.wxSize(265,315),
            wx.wxTE_MULTILINE)
    Text2=wx.wxTextCtrl(frame,51," ",--文本栏
        	wx.wxPoint(320,0),wx.wxSize(265,315),
            wx.wxTE_MULTILINE)
	menu()--菜单

	statusBar=frame:CreateStatusBar(3)--状态栏数
	frame:SetStatusText("ej与j相互转化")
	frame:SetStatusText("反馈Q:已经死了",1)
	frame:SetStatusText("用时",2)
    frame:SetIcon(wx.wxIcon("./test.ico",wx.wxBITMAP_TYPE_ICO))--设置图标

	--local optionMenu = wx.wxMenu()--复选菜单项
	--optionMenu:AppendCheckItem( 1005, "保持在顶层", "保持窗口在最上层")
	--optionMenu:Check(1005, true)--选中复选菜单项
	
	--local menuBar = wx.wxMenuBar()--菜单栏对象
	--menuBar:Append(optionMenu, "选项(&O)")
	
	--toolMenu:Enable(1006, false)--使菜单项无效
	
	--yj()--右键弹出
	--gjl()--添加工具栏
	Button()
	frame:Connect(1004, wx.wxEVT_COMMAND_MENU_SELECTED,
		function (event)
			if event:IsChecked() then
				frame:SetWindowStyle( wx.wxDEFAULT_FRAME_STYLE + wx.wxSTAY_ON_TOP )
			else
				frame:SetWindowStyle( wx.wxDEFAULT_FRAME_STYLE )
			end            
		end)
	
	--frame:Maximize(true)--最大化
    frame:Show(true)
    taskbarIcon = wx.wxTaskBarIcon()--任务栏图标对象
	taskbarIcon:SetIcon(wx.wxIcon("./test.ico",wx.wxBITMAP_TYPE_ICO), "J2EJ")--任务栏图标
	if taskbarIcon then
      taskbarIcon:delete()--删除图标
	end
end
main()
wx.wxGetApp():MainLoop()--进入循环状态
