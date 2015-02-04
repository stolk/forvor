
/*** MEMORY.C ***/

#include <stdio.h>
#include <stdlib.h>  /* malloc(), exit() */
#include <assert.h>

#include "vdefs.h"

extern int nsites, sqrt_nsites, siteidx ;

#define MAXALLOCS	128
static void* allocations[ MAXALLOCS ];
static int   numallocs=0;

void
freeinit(Freelist * fl, int size)
    {
    fl->head = (Freenode *)NULL ;
    fl->nodesize = size ;
    }

void
freeexit(void)
    {
    int i;
    for ( i=0; i<numallocs; ++i )
        {
        free( allocations[ i ] );
        allocations[ i ] = 0;
        }
    numallocs=0;
    }

char *
getfree(Freelist * fl)
    {
    int i ;
    Freenode * t ;
    if (fl->head == (Freenode *)NULL)
        {
        t =  (Freenode *) myalloc(nsites * fl->nodesize);
        for(i = 0 ; i < nsites ; i++)
            {
            makefree((Freenode *)((char *)t+i*fl->nodesize), fl) ;
            }
        }
    t = fl->head ;
    fl->head = (fl->head)->nextfree ;
    return ((char *)t) ;
    }

void
makefree(Freenode * curr, Freelist * fl)
    {
    curr->nextfree = fl->head ;
    fl->head = curr ;
    }

int total_alloc ;

char *
myalloc(unsigned n)
    {
    char * t ;
    assert(numallocs<MAXALLOCS);
    if ((t=malloc(n)) == (char *) 0)
        {
        fprintf(stderr,"Insufficient memory processing site %d (%d bytes in use)\n",
        siteidx, total_alloc) ;
        exit(0) ;
        }
    total_alloc += n ;
    allocations[numallocs++]=(void*)t;
    return (t) ;
    }
