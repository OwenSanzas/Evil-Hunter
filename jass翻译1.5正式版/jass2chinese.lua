jass2chinese=nil
function jass2chinese(t)
	starttime=os.clock()
	for _,v in pairs(trans) do
		t=string.gsub(t,v[1],v[2])
	end
	return t,os.clock()-starttime
end