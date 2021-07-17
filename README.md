# Test-and-Code-of-gem5-nvmain
主要解决了3个问题
## 1.nvmain的测试，nvmain编码算法的编写，nvmain与gem5的整合
## 2.gem5测试程序
## 3.spec cpu2006的基准程序在gem5-nvmain架构下的测试
以下将依次介绍如何实现

# 1. nvmain
首先
scons --build-type=fast
如报错，则尝试将nvmain/SConscript中的第36行注释 #from gem5_scons import Transform，因为这句暂时用不到
 
运行命令
./nvmain.fast Config/PCM_MLC_example.config Tests/Traces/hello_world.nvt 1000000

后面的配置文件，trace文件，周期数均可调整 

scons build/X86/gem5.opt
scons EXTRAS=../nvmain build/X86/gem5.opt
