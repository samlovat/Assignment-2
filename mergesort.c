/**
 * This file implements parallel mergesort.
 */

#include "mergesort.h"

#include <stdio.h>
#include <stdlib.h> /* for malloc */
#include <string.h> /* for memcpy */

/* this function will be called by mergesort() and also by parallel_mergesort().
 */
void merge(int leftstart, int leftend, int rightstart, int rightend) {
	
	int i = leftstart; // sorted segment iterator 
	int l = leftstart; // left segment iterator
	int r = rightstart;// right segment iterator

	// calculate total merge segment size for temporary array copying
	int segmentSize = rightend - leftstart + 1;

	// copy relevant memory segment to B array from A array
	memcpy(B + leftstart, A + leftstart, segmentSize * sizeof(int));


	// compare element at B[l] and B[r], moving that element into A[i] and iterating i and the respective l or r, 
	// then repeating until both l == leftend and r == rightend

	// while left or right have not iterated to the end of their respective segment
	while (l <= leftend || r <= rightend) {
		// if left iterator is not at the end, and the right value is invalid either 
		// through out of bounds or being later in the sorting chain
		if (l <= leftend && (r > rightend || B[l] <= B[r])) {
			// copy from left segment at l, and iterate l
			A[i] = B[l++];
		} else {
			// copy from left segment at r, and iterate r
			A[i] = B[r++];
		}
		i++;
	}

}

/* this function will be called by parallel_mergesort() as its base case. */
void my_mergesort(int left, int right) {

	// if splitting is valid (i.e. left is to the left of right, and not on top)
	if (left < right) {
		// divide into two equal sections, and call merge sort on those, then merge them
		int mid = (left + right) / 2;

		my_mergesort(left, mid);
		my_mergesort(mid + 1, right);
		merge(left, mid, mid + 1, right);
	}
	
}

/* this function will be called by the testing program. */
void* parallel_mergesort(void* arg) { 
	// convert the void* arg into the usable argument* type for args
	struct argument* args = (struct argument*) arg;

	// if still creating threads, create a thread,
	if (args->level < cutoff) {
		// if splitting is valid (i.e. left is to the left of right, and not on top)
		if (args->left < args->right) {
			// divide given section into two equal sections
			int mid = (args->left + args->right) / 2;

			// construct arguments for the child threads
			struct argument* argsLeft = buildArgs(args->left, mid, args->level + 1);
			struct argument* argsRight = buildArgs(mid + 1, args->right, args->level + 1);
			
			// make space to remember child threads
			pthread_t threadLeft, threadRight;

			// create threads to call mergesort on divided sections on the left and right
			pthread_create(&threadLeft, NULL, parallel_mergesort, argsLeft);
			pthread_create(&threadRight, NULL, parallel_mergesort, argsRight);

			// wait for child threads to complete mergesort on their sections
			pthread_join(threadLeft, NULL);
			pthread_join(threadRight, NULL);

			// merge the two sections sorted by merge sort and sort the combination
			merge(args->left, mid, mid + 1, args->right);
		}
	} else {
		// call merge sort without creating another thread.
		my_mergesort(args->left, args->right);
	}

	// free(args);
	return NULL;
}

/* we build the argument for the parallel_mergesort function. */
struct argument* buildArgs(int left, int right, int level) { 
	// allocate memory 
	struct argument* arg = malloc(sizeof(struct argument));

	// set values
    arg->left = left;
    arg->right = right;
    arg->level = level;

    return arg;
}
