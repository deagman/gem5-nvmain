/******************************************************************************
* Author: Hugo Zhang
* Any questions please Email HugoZhang99@outlook.com
* 		or leave message in Wbesite https://github.com/deagman
* If you want to use aFNW, you need to place this file in nvmain/DataEncoders,
* which is avilable at https://github.com/deagman/gem5-nvmain-hybrid-simulator
*******************************************************************************/

#ifndef __NVMAIN_AFNW_H__
#define __NVMAIN_AFNW_H__

#include "src/DataEncoder.h"
#include <set>

namespace NVM {

class aFNW : public DataEncoder
{
  public:
    aFNW( );
    ~aFNW( );

    void SetConfig( Config *config, bool createChildren = true );

    ncycle_t Read( NVMainRequest *request );
    ncycle_t Write( NVMainRequest *request );

    void RegisterStats( );
    void CalculateStats( );

  private:
    std::set< uint64_t > FPCAddresses;
    std::set< uint64_t > flippedAddresses1;
    std::set< uint64_t > flippedAddresses2;
    uint64_t p0;  // 统计数据
    uint64_t p1;
    uint64_t p2;
    uint64_t p3;
    uint64_t p4;
    uint64_t p5;
    uint64_t p6;
    uint64_t p7;

    uint64_t bitsFlipped;
    uint64_t bitstobeFlipped;
    uint64_t bitCompareSwapWrites;
    double aFNWReduction;

    uint64_t FPCSize;
    uint64_t fpSize;
    uint64_t curAddr;
    uint64_t Wearing[64];

    void WearOut(NVMDataBlock &data1,NVMDataBlock &data2);
    void fill_data(uint8_t *address, uint64_t index, uint64_t new_data, uint64_t data_len, uint64_t old_data, uint64_t old_raw_data);
    uint64_t CompareTwoData(uint64_t data1,uint64_t data2, uint64_t startBit, uint64_t endBit);
    uint64_t InvertData( uint64_t data, uint8_t *address, uint64_t bit_off, uint64_t data_len );
    uint64_t ChangeData(uint64_t data1, uint64_t data2, uint64_t startBit, uint64_t endBit);
};

};

#endif
