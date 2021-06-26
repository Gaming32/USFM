@echo off
for /f "tokens=1,2 delims=." %%a in (discoveringgod\lesson_list.txt) do (
 c:\php\php wrapper.php "%%b" Discovering%%a.sfm
)
