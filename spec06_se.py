from __future__ import print_function
from __future__ import absolute_import

import optparse
import sys
import os

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.params import NULL
from m5.util import addToPath, fatal, warn

addToPath('../')

from ruby import Ruby

from common import Options
from common import Simulation
from common import CacheConfig
from common import CpuConfig
#from common import ObjectList
from common import MemConfig
#from common.FileSystemConfig import config_filesystem
from common.Caches import *
from common.cpu2000 import *
import spec06_benchmarks

# Check if KVM support has been enabled, we might need to do VM
# configuration if that's the case.
have_kvm_support = 'BaseKvmCPU' in globals()
def is_kvm_cpu(cpu_class):
    return have_kvm_support and cpu_class != None and \
        issubclass(cpu_class, BaseKvmCPU)

# ...snip...
parser = optparse.OptionParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)


# NAVIGATE TO THIS POINT

# ...snip...

parser.add_option("-b", "--benchmark", type="string", default="", help="The SPEC benchmark to be loaded.")
parser.add_option("--benchmark_stdout", type="string", default="", help="Absolute path for stdout redirection for the benchmark.")
parser.add_option("--benchmark_stderr", type="string", default="", help="Absolute path for stderr redirection for the benchmark.")

def get_processes(options):
    """Interprets provided options and returns a list of processes"""

    multiprocesses = []
    outputs = []
    errouts = []

    workloads = options.benchmark.split(';')

    if options.benchmark_stdout != "":
        outputs = options.benchmark_stdout.split(';')
    elif options.output != "":
        outputs = options.output.split(';')

    if options.benchmark_stderr != "":
        errouts = options.benchmark_stderr.split(';')
    elif options.errout != "":
        errouts = options.errout.split(';')

    idx = 0
    for wrkld in workloads:

        if wrkld:
            print('Selected SPEC_CPU2006 benchmark')
            if wrkld == 'perlbench':
                print('--> perlbench')
                process = spec06_benchmarks.perlbench
            elif wrkld == 'bzip2':
                print('--> bzip2')
                process = spec06_benchmarks.bzip2
            elif wrkld == 'gcc':
                print
                '--> gcc'
                process = spec06_benchmarks.gcc
            elif wrkld == 'bwaves':
                print
                '--> bwaves'
                process = spec06_benchmarks.bwaves
            elif wrkld == 'gamess':
                print
                '--> gamess'
                process = spec06_benchmarks.gamess
            elif wrkld == 'mcf':
                print
                '--> mcf'
                process = spec06_benchmarks.mcf
            elif wrkld == 'milc':
                print
                '--> milc'
                process = spec06_benchmarks.milc
            elif wrkld == 'zeusmp':
                print
                '--> zeusmp'
                process = spec06_benchmarks.zeusmp
            elif wrkld == 'gromacs':
                print
                '--> gromacs'
                process = spec06_benchmarks.gromacs
            elif wrkld == 'cactusADM':
                print
                '--> cactusADM'
                process = spec06_benchmarks.cactusADM
            elif wrkld == 'leslie3d':
                print
                '--> leslie3d'
                process = spec06_benchmarks.leslie3d
            elif wrkld == 'namd':
                print
                '--> namd'
                process = spec06_benchmarks.namd
            elif wrkld == 'gobmk':
                print
                '--> gobmk'
                process = spec06_benchmarks.gobmk
            elif wrkld == 'dealII':
                print
                '--> dealII'
                process = spec06_benchmarks.dealII
            elif wrkld == 'soplex':
                print
                '--> soplex'
                process = spec06_benchmarks.soplex
            elif wrkld == 'povray':
                print
                '--> povray'
                process = spec06_benchmarks.povray
            elif wrkld == 'calculix':
                print
                '--> calculix'
                process = spec06_benchmarks.calculix
            elif wrkld == 'hmmer':
                print
                '--> hmmer'
                process = spec06_benchmarks.hmmer
            elif wrkld == 'sjeng':
                print
                '--> sjeng'
                process = spec06_benchmarks.sjeng
            elif wrkld == 'GemsFDTD':
                print
                '--> GemsFDTD'
                process = spec06_benchmarks.GemsFDTD
            elif wrkld == 'libquantum':
                print
                '--> libquantum'
                process = spec06_benchmarks.libquantum
            elif wrkld == 'h264ref':
                print
                '--> h264ref'
                process = spec06_benchmarks.h264ref
            elif wrkld == 'tonto':
                print
                '--> tonto'
                process = spec06_benchmarks.tonto
            elif wrkld== 'lbm':
                print
                '--> lbm'
                process = spec06_benchmarks.lbm
            elif wrkld == 'omnetpp':
                print
                '--> omnetpp'
                process = spec06_benchmarks.omnetpp
            elif wrkld == 'astar':
                print
                '--> astar'
                process = spec06_benchmarks.astar
            elif wrkld == 'wrf':
                print
                '--> wrf'
                process = spec06_benchmarks.wrf
            elif wrkld == 'sphinx3':
                print
                '--> sphinx3'
                process = spec06_benchmarks.sphinx3
            elif wrkld== 'xalancbmk':
                print
                '--> xalancbmk'
                process = spec06_benchmarks.xalancbmk
            elif wrkld == 'specrand_i':
                print
                '--> specrand_i'
                process = spec06_benchmarks.specrand_i
            elif wrkld == 'specrand_f':
                print
                '--> specrand_f'
                process = spec06_benchmarks.specrand_f
            else:
                print
                "No recognized SPEC2006 benchmark selected! Exiting."
                sys.exit(1)
            process.cwd = os.getcwd()

            if len(outputs) > idx:
                process.output = outputs[idx]
            if len(errouts) > idx:
                process.errout = errouts[idx]

            multiprocesses.append(process)
            idx += 1

        else:
            print >> sys.stderr, "Need --benchmark switch to specify SPEC CPU2006 workload. Exiting!\n"
            sys.exit(1)

    if options.smt:
        assert(options.cpu_type == "DerivO3CPU")
        return multiprocesses, idx
    else:
        return multiprocesses, 1


#parser = optparse.OptionParser()
#Options.addCommonOptions(parser)
#Options.addSEOptions(parser)

if '--ruby' in sys.argv:
    Ruby.define_options(parser)

(options, args) = parser.parse_args()

if args:
    print("Error: script doesn't take any positional arguments")
    sys.exit(1)


multiprocesses, numThreads = get_processes(options)


(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(options)
CPUClass.numThreads = numThreads

# Check -- do not allow SMT with multiple CPUs
if options.smt and options.num_cpus > 1:
    fatal("You cannot use SMT with multiple CPUs!")

np = options.num_cpus
system = System(cpu = [CPUClass(cpu_id=i) for i in range(np)],
                mem_mode = test_mem_mode,
                mem_ranges = [AddrRange(options.mem_size)],
                cache_line_size = options.cacheline_size)

if numThreads > 1:
    system.multi_thread = True

# Create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage = options.sys_voltage)

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(clock =  options.sys_clock,
                                   voltage_domain = system.voltage_domain)

# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain()

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(clock = options.cpu_clock,
                                       voltage_domain =
                                       system.cpu_voltage_domain)

# If elastic tracing is enabled, then configure the cpu and attach the elastic
# trace probe
#if options.elastic_trace_en:
#    CpuConfig.config_etrace(CPUClass, system.cpu, options)

# All cpus belong to a common cpu_clk_domain, therefore running at a common
# frequency.
for cpu in system.cpu:
    cpu.clk_domain = system.cpu_clk_domain

if is_kvm_cpu(CPUClass) or is_kvm_cpu(FutureClass):
    if buildEnv['TARGET_ISA'] == 'x86':
        system.kvm_vm = KvmVM()
        for process in multiprocesses:
            process.useArchPT = True
            process.kvmInSE = True
    else:
        fatal("KvmCPU can only be used in SE mode with x86")

# Sanity check
if options.simpoint_profile:
    if not ObjectList.is_noncaching_cpu(CPUClass):
        fatal("SimPoint/BPProbe should be done with an atomic cpu")
    if np > 1:
        fatal("SimPoint generation not supported with more than one CPUs")

for i in range(np):
    if options.smt:
        system.cpu[i].workload = multiprocesses
    elif len(multiprocesses) == 1:
        system.cpu[i].workload = multiprocesses[0]
    else:
        system.cpu[i].workload = multiprocesses[i]

    if options.simpoint_profile:
        system.cpu[i].addSimPointProbe(options.simpoint_interval)

    if options.checker:
        system.cpu[i].addCheckerCpu()

    #if options.bp_type:
    #   bpClass = ObjectList.bp_list.get(options.bp_type)
    #  system.cpu[i].branchPred = bpClass()

    #if options.indirect_bp_type:
    #    indirectBPClass = \
    #       ObjectList.indirect_bp_list.get(options.indirect_bp_type)
    #    system.cpu[i].branchPred.indirectBranchPred = indirectBPClass()

    system.cpu[i].createThreads()

if options.ruby:
    Ruby.create_system(options, False, system)
    assert(options.num_cpus == len(system.ruby._cpu_ports))

    system.ruby.clk_domain = SrcClockDomain(clock = options.ruby_clock,
                                        voltage_domain = system.voltage_domain)
    for i in range(np):
        ruby_port = system.ruby._cpu_ports[i]

        # Create the interrupt controller and connect its ports to Ruby
        # Note that the interrupt controller is always present but only
        # in x86 does it have message ports that need to be connected
        system.cpu[i].createInterruptController()

        # Connect the cpu's cache ports to Ruby
        system.cpu[i].icache_port = ruby_port.slave
        system.cpu[i].dcache_port = ruby_port.slave
        if buildEnv['TARGET_ISA'] == 'x86':
            system.cpu[i].interrupts[0].pio = ruby_port.master
            system.cpu[i].interrupts[0].int_master = ruby_port.slave
            system.cpu[i].interrupts[0].int_slave = ruby_port.master
            system.cpu[i].itb.walker.port = ruby_port.slave
            system.cpu[i].dtb.walker.port = ruby_port.slave
else:
    MemClass = Simulation.setMemClass(options)
    system.membus = SystemXBar()
    system.system_port = system.membus.slave
    CacheConfig.config_cache(options, system)
    MemConfig.config_mem(options, system)
    #config_filesystem(system, options)

#if options.wait_gdb:
#    for cpu in system.cpu:
#        cpu.wait_for_remote_gdb = True

root = Root(full_system = False, system = system)
Simulation.run(options, root, system, FutureClass)
