CFLAGS = `pkg-config --cflags gtk+-3.0` -g
LIBS = `pkg-config --libs gtk+-3.0`
LDFLAGS = 
OBJ = test-psquare.o psquare.o

test-psquare: $(OBJ)
	$(CC) -o test-psquare $(OBJ) $(LIBS) $(LDFLAGS)

clean:
	$(RM) $(OBJ) test-psquare

all: test-psquare
