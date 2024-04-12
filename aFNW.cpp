/******************************************************************************
* aFNW:先使用64位FPC对数据进行压缩，再使用FNW（分区为32位）进行位翻转，同时加入了磨损均衡
*******************************************************************************/

#include "DataEncoders/aFNW/aFNW.h"
#include <iostream>
#include <iomanip>

using namespace NVM;

static inline bool pattern_zero(int64_t x) {
    return x == 0;
}

static inline bool pattern_one(int64_t x) {
    return (x >> 7) == -1 || (x >> 7) == 0;
}

static inline bool pattern_two(int64_t x) {
    return (x >> 15) == -1 || (x >> 15) == 0;
}

static inline bool pattern_three(int64_t x) {
    return (x >> 31) == -1 || (x >> 31) == 0;
}

static inline bool pattern_four(int64_t x) {
    return (x << 32) == 0;
}

static inline bool pattern_five(int64_t x) {
    return  (((x >> (32 + 15)) == -1 || (x >> (32 + 15)) == 0)) &&
            (((x >> 15) & 0x1ffff) == 0x1ffff || ((x >> 15) & 0x1ffff) == 0);
}

// Word consisting if four repeated double bytes
static inline bool pattern_six(int64_t x) {
    int64_t repeated_double_bytes = x & 0xffff;
    int64_t expect = 0;

    expect |= repeated_double_bytes;

    expect <<= 16;
    expect |= repeated_double_bytes;

    expect <<= 16;
    expect |= repeated_double_bytes;

    expect <<= 16;
    expect |= repeated_double_bytes;

    return expect == x;
}

// uncompressed word (I commented this (By HugoZhang))
/*
static inline bool pattern_seven(int64_t x) {
    return true;
}
*/
aFNW::aFNW( )
{
    /* Clear statistics */
    p1 = 0;
    p2 = 0;
    p3 = 0;
    p4 = 0;
    p5 = 0;
    p6 = 0;
    p7 = 0;
    FPCSize = 64;
    bitsFlipped = 0;
    bitCompareSwapWrites = 0;
}
aFNW::~aFNW( )
{
    /*
     *  Nothing to do here. We do not own the *config pointer, so
     *  don't delete that.
     */
}

void aFNW::SetConfig( Config *config, bool /*createChildren*/ )
{
    Params *params = new Params( );
    params->SetParams( config );
    SetParams( params );

    // /* Cache granularity size. */
    // fpSize = config->GetValue( "FlipNWriteGranularity" );

    // /* Some default size if the parameter is not specified */
    // if( fpSize == -1 )
    //     fpSize = 32; 
}

void aFNW::RegisterStats( )
{
    AddStat(p0);
    AddStat(p1);
    AddStat(p2);
    AddStat(p3);
    AddStat(p4);
    AddStat(p5);
    AddStat(p6);
    AddStat(p7);
    AddStat(bitsFlipped);
    AddStat(bitCompareSwapWrites);
    AddUnitStat(aFNWReduction, "%");
}

ncycle_t aFNW::Read( NVMainRequest* /*request*/ )
{
    ncycle_t rv = 0;

    // TODO: Add some energy here

    return rv;
}

ncycle_t aFNW::Write( NVMainRequest *request ) 
{
    ncycle_t rv = 0;

    NVMDataBlock& newData = request->data;
    NVMDataBlock& oldData = request->oldData;
    NVMAddress address = request->address;
    uint64_t row;
    uint64_t col;
    request->address.GetTranslatedAddress( &row, &col, NULL, NULL, NULL, NULL );

    uint64_t wordSize;
    uint64_t rowSize;
    uint64_t rowPartitions;
    uint64_t FPCPartitions;


    wordSize = p->BusWidth;
    wordSize *= p->tBURST * p->RATE;
    wordSize /= 8;
    
    rowSize = p->COLS * wordSize; 	//every column has a word,which is 64*8-bit,COl = 1024, ROW = 65536
    rowPartitions = ( rowSize * 8 ) / FPCSize;
    FPCPartitions = ( wordSize * 8 ) / FPCSize;  //FPCpartitions = 8

    uint64_t byte_size = 0;
    uint64_t bit_off = 0;
    uint64_t old_data = 0;
    uint64_t new_data = 0;
    uint64_t old_raw_data = 0;

    //add a data statement (By HugoZhang)
    std::cout<<"newData oldData before FPC "<<std::endl;
    for(uint64_t i = 0;i<wordSize;i++){std::cout<<std::setfill('0')<<std::setw(2)<<std::hex<<+newData.GetByte(i);}
    std::cout<<std::endl;
    for(uint64_t i = 0;i<wordSize;i++){std::cout<<std::setfill('0')<<std::setw(2)<<std::hex<<+oldData.GetByte(i);}
    std::cout<<std::endl<<std::dec;
    

    /* Check each byte to see how many bits differ */
    for( uint64_t i = 0; i< wordSize; ++i)
    {
        /*
         *  If no bytes have changed we can just continue. Yes, I know this
         *  will check the byte 8 times, but i'd rather not change the iter.
         */
        uint8_t oldByte, newByte;

        oldByte = oldData.GetByte( i );
        newByte = newData.GetByte( i );

        if( oldByte == newByte )
        {
	    // bitTotal +=8;
	    continue;
        }
	/*
         *  If the bytes are different, then at least one bit has changed.
         *  check each bit individually.
         */
        for( int j = 0; j < 8; j++ )
	{
	    uint8_t oldBit, newBit;

            oldBit = ( oldByte >> j ) & 0x1;
            newBit = ( newByte >> j ) & 0x1;

            if( oldBit != newBit )
	    {
	        bitCompareSwapWrites ++;
	    }
	}
    }

    int64_t *ptr = (int64_t*)(newData.rawData);
    uint64_t *oldptr = (uint64_t*)(oldData.rawData);
    uint64_t i;

    while(byte_size < newData.GetSize()) {
        old_data = *ptr;
	old_raw_data = *oldptr;
        /* old_data is a 8-byte data now, but actually, the order is inverted
	 * it means only the data 7f00000000000000 will transfers into 
	 * 000000000000007f, I don't know the real situation in the computer
	 */
	std::cout<<"the data *ptr now "<<std::endl;
	std::cout.width(16);
	std::cout.fill('0');
	std::cout<<std::hex<<old_data<<std::endl;
	i = bit_off / FPCSize;
	curAddr = row * rowPartitions + col * FPCPartitions + i;
	bitstobeFlipped = 0;

        if(pattern_zero(old_data)) {
            new_data = 0;
	    /* now new_data is adapted, partition is decided by data_len,for this ,they are 2 and 1
	     * InvertData is different from the FlipNWrite.cpp
	     */
	    new_data = InvertData(new_data,oldData.rawData,bit_off,3);
            fill_data(oldData.rawData, bit_off, new_data, 3, old_data,old_raw_data);
            p0++;
            bit_off += 64;
        } else if(pattern_one(old_data)) {
            new_data = old_data & 0xff;
            new_data |= (0x1 << 8);
            /* now new_data is adapted, partition is decided by data_len,for this ,they are 6 and 5
	     * InvertData is different from the FlipNWrite.cpp
	     */
	    new_data = InvertData(new_data,oldData.rawData,bit_off,11);
            fill_data(newData.rawData, bit_off, new_data, 11, old_data,old_raw_data);
            p1++;
            bit_off += 64;
        } else if(pattern_two(old_data)) {
            new_data = old_data & 0xffff;
            new_data |= (0x2 << 16);
	    new_data = InvertData(new_data,oldData.rawData,bit_off,19);
            fill_data(newData.rawData, bit_off, new_data, 19, old_data,old_raw_data);
            p2++;
            bit_off += 64;
        } else if(pattern_three(old_data)) {
            new_data = old_data & 0xffffffff;
            new_data |= ((uint64_t)0x3 << 32);
	    new_data = InvertData(new_data,oldData.rawData,bit_off,35);
            fill_data(newData.rawData, bit_off, new_data, 35, old_data,old_raw_data);
            p3++;
            bit_off += 64;
        } else if(pattern_four(old_data)) {
            new_data = old_data >> 32;
            new_data |= ((uint64_t)0x4 << 32);
	    new_data = InvertData(new_data,oldData.rawData,bit_off,35);
            fill_data(newData.rawData, bit_off, new_data, 35, old_data,old_raw_data);
            p4++;
            bit_off += 64;
        } else if(pattern_five(old_data)) {
            new_data = old_data & 0xffff;
            new_data |= ((old_data >> 32) & 0xffff) << 16;
            new_data |= ((uint64_t)0x5 << 32);
	    new_data = InvertData(new_data,oldData.rawData,bit_off,35);
            fill_data(newData.rawData, bit_off, new_data, 35, old_data,old_raw_data);
            p5++;
            bit_off += 64;
        } else if(pattern_six(old_data)) {
            new_data = old_data & 0xffff;
            new_data |= ((uint64_t)0x6 << 16);
	    new_data = InvertData(new_data,oldData.rawData,bit_off,19);
            fill_data(newData.rawData, bit_off, new_data, 19, old_data,old_raw_data);
            p6++;
            bit_off += 64;
        } else{ // uncompressed
            new_data = old_data;
	    // I think there is no need to add a prefix(By Hugo Zhang)
	    new_data = InvertData(new_data,oldData.rawData,bit_off,64);
            fill_data(newData.rawData, bit_off, new_data, 64, old_data,old_raw_data);
            p7++;
            bit_off += 64;
        }
    
        // 下一个8 byte
        ptr++;
	oldptr++;  
        byte_size += 8;
	
    }
    
    //add a data statement (By HugoZhang)
    std::cout<<"newData oldData "<<std::endl;
    for(uint64_t i = 0;i<wordSize;i++){std::cout<<std::setfill('0')<<std::setw(2)<<std::hex<<+newData.GetByte(i);}
    std::cout<<std::endl;
    for(uint64_t i = 0;i<wordSize;i++){std::cout<<std::setfill('0')<<std::setw(2)<<std::hex<<+oldData.GetByte(i);}
    std::cout<<std::endl<<std::dec;

    WearOut(newData,oldData);
    for(uint64_t i=0; i<64; i++)
    {
	std::cout<<Wearing[i]<<" ";
    }
    std::cout<<std::endl;
    
    std::cout<<std::dec<<"bistFlipped is "<<bitsFlipped<<std::endl;
    std::cout<<std::dec<<"bitCompareSwapWrites is "<<bitCompareSwapWrites<<std::endl;

    return rv;
}

uint64_t aFNW::InvertData(uint64_t new_data,uint8_t *address,uint64_t bit_off,uint64_t data_len)
{
    uint64_t *ptr = (uint64_t*)(address + (bit_off / 8));
    uint64_t old_raw_data = *ptr;
    uint64_t InvertData=0; //this is different from the invert in FPC, and is equal to FNW's

    fpSize = (data_len-1) / 2 + 1;

    //std::cout<<"data_len - fpSize "<<data_len - fpSize<<std::endl;
    //std::cout<<"bitsDiffer "<<CompareTwoData(new_data, shift_old_raw_data, data_len - fpSize )<<std::endl;

    if ( CompareTwoData(new_data, old_raw_data>>(64-data_len), 0, data_len - fpSize) > (data_len - fpSize)/2 )
    {
	for(uint64_t i = 0; i<data_len - fpSize; i++)
	{
	    if( !( new_data>>i & 0x1) )
	    {
		InvertData |= 1UL<<i;
	    }
	}

	if( !flippedAddresses1.count( curAddr ))
        {
	    flippedAddresses1.insert( curAddr );
	    bitstobeFlipped ++;
        } 
    }
    else
    {
	for(uint64_t i = 0; i<data_len - fpSize; i++)
	{
	    if( new_data>>i & 0x1 )
	    {
		InvertData |= 1UL<<i;
	    }
	}
	if( flippedAddresses1.count( curAddr ))
        {
	    flippedAddresses1.erase( curAddr );
	    bitstobeFlipped ++;
        }
    }

    //std::cout<<"fpSize "<<fpSize<<std::endl;
    //std::cout<<"bitsDiffer "<<CompareTwoData(shift_new_data, shift_old_raw_data, fpSize )<<std::endl;

    if ( CompareTwoData(new_data, old_raw_data>>(64-data_len), data_len - fpSize, data_len ) > fpSize/2 )
    {
	
	for(uint64_t i = data_len - fpSize; i<data_len; i++)
	{
	    if( !(new_data>>i & 0x1) )
	    {
		InvertData |= 1UL<<i;
	    }
	}
	if( !flippedAddresses2.count( curAddr ))
        {
	    flippedAddresses2.insert( curAddr );
	    bitstobeFlipped ++;
        } 
    }
    else
    {
	for(uint64_t i = data_len - fpSize; i<data_len; i++)
	{
	    if( new_data>>i & 0x1 )
	    {
		InvertData |= 1UL<<i;
	    }
	}
	if( flippedAddresses2.count( curAddr ))
        {
	   flippedAddresses2.erase( curAddr );
	   bitstobeFlipped ++;
        } 
    }

    return InvertData;
}

uint64_t aFNW::CompareTwoData(uint64_t data1,uint64_t data2, uint64_t startBit, uint64_t endBit)
{
    //len means the sum of bits to compare from the lowest
    uint64_t sum = 0;
    for(uint64_t i = startBit; i < endBit; i++)
    {
	sum += (data1 >> i & 0x1) ^ (data2 >> i & 0x1);
    }
    return sum;
}
uint64_t aFNW::ChangeData(uint64_t data1, uint64_t data2, uint64_t startBit, uint64_t endBit)
{
    uint64_t shiftdata = 0;
    for(uint64_t i=0; i<startBit; i++)
    {
	shiftdata |= (data1>>i & 0x1) << i;
    }
    for(uint64_t i=startBit; i<endBit; i++)
    {
	shiftdata |= ( (data2>>(i - startBit) & 0x1) << i  );
    }
    for(uint64_t i=endBit; i<64; i++)
    {
	shiftdata |= (data1>>i & 0x1) << i;
    }
    return shiftdata;
}
void aFNW::fill_data(uint8_t *address, uint64_t bit_off, uint64_t new_data, uint64_t data_len, uint64_t old_data,uint64_t old_raw_data) 
{
    uint64_t *ptr = (uint64_t*)(address + (bit_off / 8));
    bitstobeFlipped += CompareTwoData(old_raw_data, new_data<<(64-data_len), 64-data_len, 64);
    bitstobeFlipped += (!FPCAddresses.count( curAddr ) && (data_len != 64)) || (FPCAddresses.count( curAddr ) && (data_len == 64));

    if( bitstobeFlipped < CompareTwoData(old_raw_data,old_data,0,64) )
    {
	*ptr = ChangeData(old_raw_data, new_data, 64-data_len, 64 );
	bitsFlipped +=bitstobeFlipped;
	if(data_len == 64) FPCAddresses.erase( curAddr );
	else FPCAddresses.insert( curAddr );
	std::cout<<"compressed"<<std::endl;
    }
    else
    {
	//*ptr = old_data;
	bitsFlipped += CompareTwoData(old_raw_data,old_data,0,64);
	if(FPCAddresses.count( curAddr ))
	{ 
	    FPCAddresses.erase( curAddr );
	    bitsFlipped ++;
	}
	std::cout<<"decompressed"<<std::endl;
    }
}
void aFNW::WearOut(NVMDataBlock& newData, NVMDataBlock& oldData)
{
    for(uint64_t i = 0; i<64; i++)
    {
	for(uint64_t j = 0; j<8; j++)
	{
	    Wearing[ (i*8 + j) / 8 ] += (newData.GetByte(i) >> j & 0x1) ^ (oldData.GetByte(i) >> j & 0x1);
	}
    }
}
void aFNW::CalculateStats( )
{
    if( bitCompareSwapWrites != 0 )
        aFNWReduction = (((double)bitsFlipped / (double)bitCompareSwapWrites)*100.0);
    else
        aFNWReduction = 100.0
}
