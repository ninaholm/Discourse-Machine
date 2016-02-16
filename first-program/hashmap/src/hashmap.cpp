/*
CSTHASH - template for hash class

Copyright (C) 2012 Center for Sprogteknologi, University of Copenhagen

This file is part of CSTHASH.

CSTHASH is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

CSTHASH is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CSTHASH; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#include "hashmap.h"

size_t hashmap::nextprime(size_t g)
    {
    int i;
    size_t smalldivisor;
    static int byte[12]=
        {1,  2,  2,  4,    2,    4,    2,    4,    6,    2,  6};
    /*2-3,3-5,5-7,7-11,11-13,13-17,17-19,19-23,23-29,29-1,1-7*/
    /*unsigned*/ size_t bigdivisor;
    if(g & 1)
        ++g; /* even -> uneven */
    smalldivisor = 2;
    i = 0;
    while((bigdivisor = g / smalldivisor) >= smalldivisor)
        {
        if(bigdivisor * smalldivisor == g)
            {
            ++g;
            smalldivisor = 2;
            i = 0;
            }
        else
            {
            smalldivisor += byte[i];
            if(++i > 10)
                i = 3;
            }
        }
    return g;
    }


size_t hashmap::casesensitivehash(const char * cp)
    {
    size_t hash_temp = 0;
    while (*cp != '\0')
        {
		hash_temp = 31 * hash_temp + *cp;
        ++cp;
        }
    return hash_temp;
    }

