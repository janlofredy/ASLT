Dim Shell

Set Shell = CreateObject("Wscript.shell")
requirementsPath = "conf.bat"
Shell.Run requirementsPath
'Clean up