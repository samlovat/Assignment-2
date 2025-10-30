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

	int i = leftstart;
	int l = leftstart;
	int r = rightstart;

	int segmentSize = rightend - leftstart + 1;

	memcpy(B + leftstart, A + leftstart, segmentSize * sizeof(int));

	while (l <= leftend || r <= rightend) {
		if (l <= leftend && (r > rightend || B[l] <= B[r])) {
			A[i] = B[l++];
		} else {
			A[i] = B[r++];
		}
		i++;
	}

}

/* this function will be called by parallel_mergesort() as its base case. */
void my_mergesort(int left, int right) {

	if (left < right) {
		int mid = (left + right) / 2;

		my_mergesort(left, mid);
		my_mergesort(mid + 1, right);
		merge(left, mid, mid + 1, right);
	}
	
}

/* this function will be called by the testing program. */
void* parallel_mergesort(void* arg) { 
	struct argument* args = (struct argument*) arg;

	if (args->level < cutoff) {
		if (args->left < args->right) {
			int mid = (args->left + args->right) / 2;

			struct argument* argsLeft = buildArgs(args->left, mid, args->level + 1);
			struct argument* argsRight = buildArgs(mid + 1, args->right, args->level + 1);
			
			pthread_t threadLeft, threadRight;

			pthread_create(&threadLeft, NULL, parallel_mergesort, argsLeft);
			pthread_create(&threadRight, NULL, parallel_mergesort, argsRight);

			pthread_join(threadLeft, NULL);
			pthread_join(threadRight, NULL);

			merge(args->left, mid, mid + 1, args->right);
		}
	} else {
		my_mergesort(args->left, args->right);
	}

	// free(args);
	return NULL;
}

/* we build the argument for the parallel_mergesort function. */
struct argument* buildArgs(int left, int right, int level) { 
	struct argument* arg = malloc(sizeof(struct argument));

    arg->left = left;
    arg->right = right;
    arg->level = level;

    return arg;
}
