CC=clang
CFLAGS=-g -Wall -Isrc


LIBOBJS=\
src/edgelist.o \
src/geometry.o \
src/heap.o \
src/memory.o \
src/output.o \
src/voronoi.o

MAINOBJ=\
test/main.o

all: testforvor testrun


libforvor.a: $(LIBOBJS)
	ar rcsv $*.a $(LIBOBJS)

testforvor: libforvor.a $(MAINOBJ)
	$(CC) $(MAINOBJ) -otestforvor -L. -lforvor -lm

testrun:
	tail -1024 testdata/2,3-halton.points | ./testforvor > testrun.diagram
	cat testrun.diagram | tools/mkpoly.py > testrun.poly
	cat testrun.poly | tools/mksvg.py > testrun.svg
	-inkscape testrun.svg

leakcheck:
	valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all ./testforvor < testdata/2,3-halton.points > testrun.diagram

clean:
	rm -f *.a
	rm -f $(LIBOBJS)
	rm -f testforvor

