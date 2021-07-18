# Test-and-Code-of-gem5-nvmain
# Author: HugoZhang 
# Date: 2021.4
### Any questions please Email HugoZhang99@outlook.com or leave message in Website https://github.com/deagman
主要解决了3个问题
## 1.nvmain的测试，nvmain编码算法的编写，nvmain与gem5的整合
## 2.gem5测试程序
## 3.spec cpu2006的基准程序在gem5-nvmain架构下的测试
以下将依次介绍如何实现

nvmain和gem5的相关文献
https://www.jianshu.com/p/af2efe552a11

## nvmain和gem5两者处在同一个目录下，避免路径问题

## 1. nvmain
首先，nvmain的官网早就没了，本身软件也早在很多年前就停止更新了，网上能够找到nvmain相关的使用屈指可数，重复引用实在是太多了。因此希望找到更好的参考文献是徒劳的。
### 1.1 nvmain的下载和编译
gem5和nvmain的资源都在此：
https://github.com/deagman/gem5-nvmain-hybrid-simulator
（需要注意的是，这里的gem5里py部分是用python2编写的）

开始编译nvmain，在此之前需要先安装scons，一个py编写的编译工具，相当于makefile的作用，而在gem5中同样也需要用到。
scons直接安装就好了，跟此时环境的py版本无关。但是在编译时，需要指定好py版本，例如gem5有py2和py3版本的，在使用scons编译gem5时，需要py版本环境对应。如果你下载的就是上方资源，则直接从头到尾使用py2就好了。实际上在编译gem5的py3版本时（官网上就是py3版本），我切换至py3环境gem5仍会提示py版本过低，原因不明。

进入nvmain目录，编译，这里编译有3种类型fast|debug|prof，选择fast就好了

scons --build-type=fast

（如报错，则尝试将nvmain/SConscript中的第36行注释 #from gem5_scons import Transform，因为这句暂时用不到。这句是在gem5中导入nvmain时才需要，相当于在gem5中添加非易失性内存的类）
 
### 1.2 nvmain的运行
./nvmain.fast Config/PCM_MLC_example.config Tests/Traces/hello_world.nvt 1000000

Config/PCM_MLC_example.config为配置文件，配置文件里设置了内存的诸多参数，如能量、延迟、容量、行列规格等等，还可以自己添加参数进去（编码算法中会提到）
Tests/Traces/hello_world.nvt为trace文件，就是内存条中每个存储周期内某个地址发生的读写变化，格式为**CYCLE OP ADDRESS DATA OLDDATA THREADID**。仔细理解traceReader和traceWriter文件，里面提到了nvmain如何读取和生成trace文件。
1000000 为周期数，简单点说，代表周期越多，trace跑的越多

配置文件大同小异，我的测试都是使用Config/PCM_MLC_example.config文件，主要改变的是1.编码算法种类参数，2.算法中需要的不同参数。详情见PCM_MLC_example.config
### 1.3 nvmain的trace文件
trace文件nvmain只提供了一个，要生成自己的trace文件的话，需要和gem5结合（gem5运行程序，将数据传输给nvmain，修改配置文件中的参数生成trace），后面会解释如何生成自己的trace。
自带的hello_world.nvt，就是一个简单的hello.c程序跑出来的

简单介绍如何打印trace文件
**trace文件首的NVMV0表示默认olddata都是0，NVMV1下才会读取olddata（具体在traceReader可见）**

**修改PCM_MLC_example.config中PrintPreTrace为true**具体如下

; Simulation control parameters

PrintPreTrace false --》true

PreTraceFile pcm.trace --生成的trace文件名

**测试hello_world.nvt**
会发现Config生成了pcm.trace文件。

nvmain中的trace只是一个展示功能而已，nvmain也不能真的对内存条进行操作。换而言之，对trace中同一个地址连续写两次数据，下一次的旧数据并不会是上一次写的数据。例如：

0 0x1 W ffff 0000（对1地址写ffff，旧数据为0000）（这里为了表示简单忽略了格式）

1 0x1 W 0001 0000 (对1地址写0001，旧数据为0000)

这两者并不会有任何矛盾，因为nvmain并没有真的维护一个内存空间。

### 1.4 nvmain的编码算法
具体见
https://www.jianshu.com/p/af2efe552a11

实际上nvmain作者本身也写了FNW算法，仔细理解，就会知道一个编码算法如何去写。实际简书也是抄的作者代码。作者FNW有2个问题
1.反转函数写错了
2.在写新数据时，不需要根据标志位反转旧数据了，因为旧数据已经是真实地写好了，写的时候，FNW不关心旧数据反转与否，顶多是计较一下标志位反转

参考资料简书中的FPC算法是有压缩空间这一个步骤的，这是内存块级别才有的，不过根据相关论文中的意思，这个压缩方式是错的，应当把前缀都放在一起

实际上FPC在字级别的上并不会压缩数据，如果读懂了简书中的算法，想必不压缩空间的FPC也能容易实现。此外，这里的FPC没有考虑标志位反转，实际上考虑的话是一件很麻烦的事。

这里提供修改好的FNW，可以测试一下FNW执行 0 0x1 W ffff 0000 时，NVMV1下生成pcm.trace里会变成0 0x1 W 0000 0000，这里表明FNW将新数据ffff反转成0000了
也顺便提供一下FPC的测试trace，注意新旧数据之间有一个空格。

## 2. gem5
### 2.1 gem5编译与测试
gem5下载编译在https://www.jianshu.com/p/af2efe552a11
编译会花很长时间，大概30分钟。

gem5测试命令

./build/X86/gem5.opt configs/example/se.py -c tests/test-progs/hello/bin/x86/linux/hello

py文件内有CPU和cache的配置，-c 为模拟程序。gem5命令中的相关参数可调的非常多，具体可见gem5官网。
### 2.2 nvmain 和 gem5结合
将nvmain/SConscript中的第36行取消注释 from gem5_scons import Transform
在gem5目录下

scons EXTRAS=../nvmain build/X86/gem5.opt

此时gem5.opt有--mem-type=NVMainMemory

./build/X86/gem5.opt configs/example/se.py -c tests/test-progs/hello/bin/x86/linux/hello --mem-type=NVMainMemory --nvmain-config=../nvmain/Config/PCM_MLC_example.config

运行成功则表示内存类型可选择NVmain了

### 2.3 gem5-nvmain运行程序生成trace
2.2中的程序tests/test-progs/hello/bin/x86/linux/hello是一个**静态编译**的c文件，你可以编写自己的程序。不过这里的程序最好不要带参数的输入，而需要输入参数的程序，具体见官网。

为了能够运行自己的程序并生成trace文件，需要加入更多的gem5参数，如下

./build/X86/gem5.opt ./configs/example/se.py -c tests/test-progs/hello/bin/x86/linux/hello --cpu-type=TimingSimpleCPU --mem-type=NVMainMemory --nvmain-config=../nvmain/Config/PCM_MLC_example.config --caches --cacheline_size=64 --l2cache --l1i_size 32kB --l1d_size 32kB --l2_size 256kB

PCM_MLC_example.config的打印参数为真。这里重要的是的是**TimingSimpleCPU**，**cacheline_size=64**。前者决定CPU类型，后者的64表示一个块是64字节，和nvmain的默认内存块大小一致，以上命令可以生成trace文件

## 3.spec cpu2006
spec安装和运行教程如下https://blog.csdn.net/qq_38877888/article/details/108759538
（虽然这个也是外网的）

里面提到了3个脚本文件，实际上由于各种版本原因，脚本有些地方要删改

我的目录结构为 speccpu2006,bishe/nvmain,bishe/gem5，脚本写好后在gem5下执行：

sudo ./run_gem5_amd64_spec06_benchmarks.sh bzip2 /home/zcq/bishe/gem5/m5out/spec

run.sh中关键部分如下，其中-I表示指令运行总数，之前设定为10亿，大概一个程序要跑30分钟。后来将run.sh中运行脚本输出屏蔽了，不然会一直生成输入信息，文件会很大几十个G。这里跑程序时也不要打印trace了，trace会非常大。

$GEM5_DIR/build/$ARCH/gem5.opt \
$GEM5_DIR/configs/example/spec06_se.py \
--benchmark=$BENCHMARK \
--benchmark_stdout=$OUTPUT_DIR/$BENCHMARK.out \
--benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err \
--num-cpus=1 \
--cpu-type=TimingSimpleCPU \
--cpu-clock=2.8GHz \
--caches \
--cacheline_size=64 \
--l1d_size=32kB --l1i_size=32kB \
--l2cache --l2_size=2MB \
--mem-type=NVMainMemory \
--nvmain-config=../nvmain/Config/PCM_MLC_example.config \
--mem-size=4096MB \
-I 200000000 \
| tee -a $SCRIPT_OUT
