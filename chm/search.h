#ifndef CHM_SEARCH_H
#define CHM_SEARCH_H

#include <chm_lib.h>

typedef int (*search_cb)(const char *topic, const char *url, void *context);

int search(struct chmFile *chmfile, const char *text, int whole_words,
           int titles_only, search_cb cb, void *context);

#endif
