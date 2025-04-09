CC=gcc
CFLAGS=-Wall -Wextra

all: neural_reader

neural_reader: main.c process.c
	$(CC) $(CFLAGS) -o neural_reader main.c process.c

clean:
	rm -f neural_reader

.PHONY: all clean 