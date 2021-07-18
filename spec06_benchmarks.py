import m5
from m5.objects import *

# These three directory paths are not currently used.
GEM5_DIR = '/home/zcq/bishe/gem5/'
SPEC_DIR = '/home/zcq/speccpu2006/benchspec/CPU2006/'
out_dir = '/home/zcq/bishe/gem5/m5out/spec'

dir_suffix='/run/run_base_ref_gcc43-64bit.0000/'
exe_suffix = '_base.gcc43-64bit'

#temp
#binary_dir = spec_dir
#data_dir = spec_dir

#400.perlbench
perlbench = Process(pid=400)
fullpath=SPEC_DIR+'400.perlbench'+dir_suffix
perlbench.executable = fullpath + 'perlbench' + exe_suffix
# TEST CMDS
#perlbench.cmd = [perlbench.executable] + ['-I.', '-I./lib', 'attrs.pl']
# REF CMDS
perlbench.cmd = [perlbench.executable] + ['-I'+fullpath+'/lib',fullpath+'/checkspam.pl', '2500', '5', '25', '11', '150', '1', '1', '1', '1']
#perlbench.cmd = [perlbench.executable] + ['-I./lib', 'diffmail.pl', '4', '800', '10', '17', '19', '300']
#perlbench.cmd = [perlbench.executable] + ['-I./lib', 'splitmail.pl', '1600', '12', '26', '16', '4500']
#perlbench.output = out_dir+'perlbench.out'

#401.bzip2
bzip2 = Process(pid=401)
fullpath=SPEC_DIR+'401.bzip2'+dir_suffix
bzip2.executable = fullpath + 'bzip2' + exe_suffix
# TEST CMDS
#bzip2.cmd = [bzip2.executable] + ['input.program', '5']
# REF CMDS
bzip2.cmd = [bzip2.executable] + [fullpath+'input.source', '280']
#bzip2.cmd = [bzip2.executable] + ['chicken.jpg', '30']
#bzip2.cmd = [bzip2.executable] + ['liberty.jpg', '30']
#bzip2.cmd = [bzip2.executable] + ['input.program', '280']
#bzip2.cmd = [bzip2.executable] + ['text.html', '280']
#bzip2.cmd = [bzip2.executable] + ['input.combined', '200']
#bzip2.output = out_dir + 'bzip2.out'

# 403.gcc
gcc = Process(pid=403)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'403.gcc'+dir_suffix
gcc.executable = fullpath+'gcc' + exe_suffix
# TEST CMDS
# gcc.cmd = [gcc.executable] + [fullpath+'cccp.in', '-o',fullpath+ 'cccp.s']
# REF CMDS
gcc.cmd = [gcc.executable] + [fullpath+'166.in', '-o', fullpath+'166.s']
# gcc.cmd = [gcc.executable] + [fullpath+'200.in', '-o',fullpath+ '200.s']
# gcc.cmd = [gcc.executable] + [fullpath+'c-typeck.in', '-o',fullpath+ 'c-typeck.s']
# gcc.cmd = [gcc.executable] + [fullpath+'cp-decl.in', '-o',fullpath+ 'cp-decl.s']
# gcc.cmd = [gcc.executable] + [fullpath+'expr.in', '-o',fullpath+ 'expr.s']
# gcc.cmd = [gcc.executable] + [fullpath+'expr2.in', '-o',fullpath+ 'expr2.s']
# gcc.cmd = [gcc.executable] + [fullpath+'g23.in', '-o',fullpath+ 'g23.s']
# gcc.cmd = [gcc.executable] + [fullpath+'s04.in', '-o',fullpath+ 's04.s']
# gcc.cmd = [gcc.executable] + [fullpath+'scilab.in', '-o',fullpath+ 'scilab.s']
# gcc.output = out_dir + 'gcc.out'

# 410.bwaves
bwaves = Process(pid=410)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'410.bwaves'+dir_suffix
bwaves.executable = fullpath+'bwaves' + exe_suffix
# TEST CMDS
# bwaves.cmd = [bwaves.executable]
# REF CMDS
bwaves.cmd = [bwaves.executable]
# bwaves.output = out_dir + 'bwaves.out'

# 416.gamess
gamess = Process(pid=416)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'416.gamess'+dir_suffix
gamess.executable = fullpath+'gamess' + exe_suffix
# TEST CMDS
# gamess.cmd = [gamess.executable]
# gamess.input = fullpath+'exam29.config'
# REF CMDS
gamess.cmd = [gamess.executable]
gamess.input = fullpath+'cytosine.2.config'
# gamess.cmd = [gamess.executable]
# gamess.input = fullpath+'h2ocu2+.gradient.config'
# gamess.cmd = [gamess.executable]
# gamess.input = fullpath+'triazolium.config'
# gamess.output = out_dir + 'gamess.out'

# 429.mcf
mcf = Process(pid=429)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'429.mcf'+dir_suffix
mcf.executable = fullpath+'mcf' + exe_suffix
# TEST CMDS
# mcf.cmd = [mcf.executable] + [fullpath+'inp.in']
# REF CMDS
mcf.cmd = [mcf.executable] + [fullpath+'inp.in']
# mcf.output = out_dir + 'mcf.out'

# 433.milc
milc = Process(pid=433)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'433.milc'+dir_suffix
milc.executable = fullpath+'milc' + exe_suffix
# TEST CMDS
# milc.cmd = [milc.executable]
# milc.input = fullpath+'su3imp.in'
# REF CMDS
milc.cmd = [milc.executable]
milc.input = fullpath+'su3imp.in'
# milc.output = out_dir + 'milc.out'

# 434.zeusmp
zeusmp = Process(pid=434)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'434.zeusmp'+dir_suffix
zeusmp.executable = fullpath+'zeusmp' + exe_suffix
# TEST CMDS
# zeusmp.cmd = [zeusmp.executable]
# REF CMDS
zeusmp.cmd = [zeusmp.executable]
# zeusmp.output = out_dir + 'zeusmp.out'

# 435.gromacs
gromacs = Process(pid=435)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'435.gromacs'+dir_suffix
gromacs.executable = fullpath+'gromacs' + exe_suffix
# TEST CMDS
# gromacs.cmd = [gromacs.executable] + ['-silent','-deffnm',fullpath+ 'gromacs', '-nice','0']
# REF CMDS
gromacs.cmd = [gromacs.executable] + ['-silent', '-deffnm', fullpath+'gromacs', '-nice', '0']
# gromacs.output = out_dir + 'gromacs.out'

# 436.cactusADM
cactusADM = Process(pid=436)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'436.cactusADM'+dir_suffix
cactusADM.executable = fullpath+'cactusADM' + exe_suffix
# TEST CMDS
# cactusADM.cmd = [cactusADM.executable] + [fullpath+'benchADM.par']
# REF CMDS
cactusADM.cmd = [cactusADM.executable] + [fullpath+'benchADM.par']
# cactusADM.output = out_dir + 'cactusADM.out'

# 437.leslie3d
leslie3d = Process(pid=437)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'437.leslie3d'+dir_suffix
leslie3d.executable = fullpath+'leslie3d' + exe_suffix
# TEST CMDS
# leslie3d.cmd = [leslie3d.executable]
# leslie3d.input = fullpath+'leslie3d.in'
# REF CMDS
leslie3d.cmd = [leslie3d.executable]
leslie3d.input = fullpath+'leslie3d.in'
# leslie3d.output = out_dir + 'leslie3d.out'

# 444.namd
namd = Process(pid=444)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'444.namd'+dir_suffix
namd.executable = fullpath+'namd' + exe_suffix
# TEST CMDS
# namd.cmd = [namd.executable] + ['--input', fullpath+'namd.input', '--output', fullpath+'namd.out', '--iterations', '1']
# REF CMDS
namd.cmd = [namd.executable] + ['--input', fullpath+'namd.input', '--output', fullpath+'namd.out', '--iterations', '38']
# namd.output = out_dir + 'namd.out'

# 445.gobmk
gobmk = Process(pid=445)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'445.gobmk'+dir_suffix
gobmk.executable = fullpath+'gobmk' + exe_suffix
# TEST CMDS
# gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
# gobmk.input = fullpath+'dniwog.tst'
# REF CMDS
gobmk.cmd = [gobmk.executable] + ['--quiet', '--mode', 'gtp']
gobmk.input = fullpath+'13x13.tst'
# gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
# gobmk.input = fullpath+'nngs.tst'
# gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
# gobmk.input = fullpath+'score2.tst'
# gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
# gobmk.input = fullpath+'trevorc.tst'
# gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
# gobmk.input = fullpath+'trevord.tst'
# gobmk.output = out_dir + 'gobmk.out'

# 447.dealII
####### NOT WORKING #########
dealII = Process(pid=447)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'447.dealII'+dir_suffix
dealII.executable = fullpath+'dealII' + exe_suffix
# TEST CMDS
####### NOT WORKING #########
dealII.cmd = [gobmk.executable]+['8']
# REF CMDS
####### NOT WORKING #########
# dealII.output = out_dir + 'dealII.out'

# 450.soplex
soplex = Process(pid=450)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'450.soplex'+dir_suffix
soplex.executable = fullpath+'soplex' + exe_suffix
# TEST CMDS
# soplex.cmd = [soplex.executable] + ['-m10000',fullpath+ 'test.mps']
# REF CMDS
soplex.cmd = [soplex.executable] + ['-m45000', fullpath+'pds-50.mps']
# soplex.cmd = [soplex.executable] + ['-m3500', fullpath+'ref.mps']
# soplex.output = out_dir + 'soplex.out'

# 453.povray
povray = Process(pid=453)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'453.povray'+dir_suffix
povray.executable = fullpath+'povray' + exe_suffix
# TEST CMDS
# povray.cmd = [povray.executable] + [fullpath+'SPEC-benchmark-test.ini']
# REF CMDS
povray.cmd = [povray.executable] + [fullpath+'SPEC-benchmark-ref.ini']
povray.output = out_dir + 'povray.out'

# 454.calculix
calculix = Process(pid=454)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'454.calculix'+dir_suffix
calculix.executable = fullpath+'calculix' + exe_suffix
# TEST CMDS
# calculix.cmd = [calculix.executable] + ['-i', 'beampic']
# REF CMDS
calculix.cmd = [calculix.executable] + ['-i', 'hyperviscoplastic']
# calculix.output = out_dir + 'calculix.out'

# 456.hmmer
hmmer = Process(pid=456)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'456.hmmer'+dir_suffix
hmmer.executable = fullpath+'hmmer' + exe_suffix
# TEST CMDS
# hmmer.cmd = [hmmer.executable] + ['--fixed', '0', '--mean', '325', '--num', '45000', '--sd', '200', '--seed', '0', fullapth+'bombesin.hmm']
# REF CMDS
hmmer.cmd = [hmmer.executable] + [fullpath+'nph3.hmm', fullpath+'swiss41']
# hmmer.cmd = [hmmer.executable] + ['--fixed', '0', '--mean', '500', '--num', '500000', '--sd', '350', '--seed', '0', fullpath+'retro.hmm']
# hmmer.output = out_dir + 'hmmer.out'

# 458.sjeng
sjeng = Process(pid=458)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'458.sjeng'+dir_suffix
sjeng.executable = fullpath+'sjeng' + exe_suffix
# TEST CMDS
# sjeng.cmd = [sjeng.executable] + [fullpath+'test.txt']
# REF CMDS
sjeng.cmd = [sjeng.executable] + [fullpath+'ref.txt']
# sjeng.output = out_dir + 'sjeng.out'

# 459.GemsFDTD
GemsFDTD = Process(pid=459)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'459.GemsFDTD'+dir_suffix
GemsFDTD.executable = fullpath+'GemsFDTD' + exe_suffix
# TEST CMDS
# GemsFDTD.cmd = [GemsFDTD.executable]
# REF CMDS
GemsFDTD.cmd = [GemsFDTD.executable]
# GemsFDTD.output = out_dir + 'GemsFDTD.out'

# 462.libquantum
libquantum = Process(pid=462)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'462.libquantum'+dir_suffix
libquantum.executable = fullpath+'libquantum' + exe_suffix
# TEST CMDS
# libquantum.cmd = [libquantum.executable] + ['33','5']
# REF CMDS [UPDATE 10/2/2015]: Sparsh Mittal has pointed out the correct input for libquantum should be 1397 and 8, not 1297 and 8. Thanks!
libquantum.cmd = [libquantum.executable] + ['1397', '8']
# libquantum.output = out_dir + 'libquantum.out'

# 464.h264ref
h264ref = Process(pid=464)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'464.h264ref'+dir_suffix
h264ref.executable = fullpath+'h264ref' + exe_suffix
# TEST CMDS
# h264ref.cmd = [h264ref.executable] + ['-d', fullpath+'foreman_test_encoder_baseline.cfg']
# REF CMDS
h264ref.cmd = [h264ref.executable] + ['-d', fullpath+'foreman_ref_encoder_baseline.cfg']
# h264ref.cmd = [h264ref.executable] + ['-d', fullpath+'foreman_ref_encoder_main.cfg']
# h264ref.cmd = [h264ref.executable] + ['-d', fullpath+'sss_encoder_main.cfg']
# h264ref.output = out_dir + 'h264ref.out'

# 465.tonto
tonto = Process(pid=465)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'465.tonto'+dir_suffix
tonto.executable = fullpath+'tonto' + exe_suffix
# TEST CMDS
# tonto.cmd = [tonto.executable]
# REF CMDS
tonto.cmd = [tonto.executable]
# tonto.output = out_dir + 'tonto.out'

# 470.lbm
lbm = Process(pid=470)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'470.lbm'+dir_suffix
lbm.executable = fullpath+'lbm' + exe_suffix
# TEST CMDS
# lbm.cmd = [lbm.executable] + ['20', fullpath+'reference.dat', '0', '1', fullpath+'100_100_130_cf_a.of']
# REF CMDS
lbm.cmd = [lbm.executable] + ['300', fullpath+'reference.dat', '0', '0', fullpath+'100_100_130_ldc.of']
# lbm.output = out_dir + 'lbm.out'

# 471.omnetpp
omnetpp = Process(pid=471)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'471.omnetpp'+dir_suffix
omnetpp.executable = fullpath+'omnetpp' + exe_suffix
# TEST CMDS
# omnetpp.cmd = [omnetpp.executable] + [fullpath+'omnetpp.ini']
# REF CMDS
omnetpp.cmd = [omnetpp.executable] + [fullpath+'omnetpp.ini']
# omnetpp.output = out_dir + 'omnetpp.out'

# 473.astar
astar = Process(pid=473)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'473.astar'+dir_suffix
astar.executable = fullpath+'astar' + exe_suffix
# TEST CMDS
# astar.cmd = [astar.executable] + [fullpath+'lake.cfg']
# REF CMDS
astar.cmd = [astar.executable] + [fullpath+'rivers.cfg']
# astar.output = out_dir + 'astar.out'

# 481.wrf
wrf = Process(pid=481)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'481.wrf'+dir_suffix
wrf.executable = fullpath+'wrf' + exe_suffix
# TEST CMDS
# wrf.cmd = [wrf.executable]
# REF CMDS
wrf.cmd = [wrf.executable]
# wrf.output = out_dir + 'wrf.out'

# 482.sphinx3
sphinx3 = Process(pid=482)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'482.sphinx3'+dir_suffix
sphinx3.executable = fullpath+'sphinx_livepretend' + exe_suffix
# TEST CMDS
# sphinx3.cmd = [sphinx3.executable] + [fullpath+'ctlfile', fullpath, fullpath+'args.an4']
# REF CMDS
sphinx3.cmd = [sphinx3.executable] + [fullpath+'ctlfile', fullpath, fullpath+'args.an4']
# sphinx3.output = out_dir + 'sphinx3.out'

# 483.xalancbmk
######## NOT WORKING ###########
xalancbmk = Process(pid=483)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'483.xalancbmk'+dir_suffix
xalancbmk.executable = fullpath+'Xalan' + exe_suffix
# TEST CMDS
######## NOT WORKING ###########
xalancbmk.cmd = [xalancbmk.executable] + ['-v',fullpath+'test.xml',fullpath+'xalanc.xsl']
# REF CMDS
######## NOT WORKING ###########
# xalancbmk.output = out_dir + 'xalancbmk.out'

# 998.specrand
specrand_i = Process(pid=998)  # Update June 7, 2017: This used to be LiveProcess()
fullpath=SPEC_DIR+'998.specrand'+dir_suffix
specrand_i.executable = fullpath+'specrand' + exe_suffix
# TEST CMDS
# specrand_i.cmd = [specrand_i.executable] + ['324342', '24239']
# REF CMDS
specrand_i.cmd = [specrand_i.executable] + ['1255432124', '234923']
# specrand_i.output = out_dir + 'specrand_i.out'
# 999.specrand
specrand_f = Process(pid=999)  # Update June 7, 2017: This used to be LiveProces using std::in;
fullpath=SPEC_DIR+'999.specrand'+dir_suffix
specrand_f.executable = fullpath+'specrand' + exe_suffix
# TEST CMDS
# specrand_f.cmd = [specrand_f.executable] + ['324342', '24239']
# REF CMDS
specrand_f.cmd = [specrand_f.executable] + ['1255432124', '234923']
# specrand_f.output = out_dir + 'specrand_f.out'
