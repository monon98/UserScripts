@echo off
chcp 65001 > nul

:menu
echo 自定义docker-compose菜单

setlocal enabledelayedexpansion
set index=1

for /D %%d in (*) do (
  echo [!index!] %%d
  set /A index+=1
)

echo [0] 退出程序

set /p input=请输入编号：
set /A input=%input% 2>nul

cls
if "%input%" NEQ "" (
  if %input% GTR 0 (
    set validChoice=false
    set index=1
    for /D %%d in (*) do (
      if !index! EQU %input% (
        set validChoice=true
        
        cls
        setlocal disabledelayedexpansion
        
        echo 执行结果：
        echo.
        
        echo 执行命令：cd "%%d" ^&^& docker-compose -f "%%~nd.yml" up -d

        cd "%%d" && docker-compose -f "%%~nd.yml" up -d && cd ..
        
        set done=true
        
        echo.
        echo **命令已执行完毕！**
        echo.
        timeout /t 3 > nul
        goto menu
      )
      
      set /A index+=1
    )
    
    endlocal
    
    if "%validChoice%"=="false" (
      echo 无效的编号，请重新输入编号。
      timeout /t 3 > nul
      goto menu
    )
    
    goto menu
  ) else if %input% EQU 0 (
    exit
  )
) else (
  echo 无效的编号，请重新输入编号。
  timeout /t 3 > nul
  goto menu
)