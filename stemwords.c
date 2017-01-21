/* This is a simple program which uses libstemmer to provide a command
 * line interface for stemming using any of the algorithms provided.
 */

#include <stdio.h>
#include <stdlib.h> /* for malloc, free */
#include <string.h> /* for memmove */
#include <ctype.h>  /* for isupper, tolower */

#include "libstemmer.h"

//const char * progname;
static int pretty = 1;

static void
stem_file(struct sb_stemmer * stemmer, FILE * f_in, FILE * f_out)
{
#define INC 10
    int lim = INC;
    sb_symbol * b = (sb_symbol *) malloc(lim * sizeof(sb_symbol));

    while(1) {
        int ch = getc(f_in);
        if (ch == EOF) {
            free(b); return;
        }
        {
            int i = 0;
	    int inlen = 0;
            while(1) {
                if (ch == '\n' || ch == EOF) break;
                if (i == lim) {
                    sb_symbol * newb;
		    newb = (sb_symbol *)
			    realloc(b, (lim + INC) * sizeof(sb_symbol));
		    if (newb == 0) goto error;
		    b = newb;
                    lim = lim + INC;
                }
		/* Update count of utf-8 characters. */
		if (ch < 0x80 || ch > 0xBF) inlen += 1;
                /* force lower case: */
                if (isupper(ch)) ch = tolower(ch);

                b[i] = ch;
		i++;
                ch = getc(f_in);
            }

	    {
		const sb_symbol * stemmed = sb_stemmer_stem(stemmer, b, i);
                if (stemmed == NULL)
                {
                    fprintf(stderr, "Out of memory");
                    exit(1);
                }
                else
		{
		    if (pretty == 1) {
			fwrite(b, i, 1, f_out);
			fputs(" -> ", f_out);
		    } else if (pretty == 2) {
			fwrite(b, i, 1, f_out);
			if (sb_stemmer_length(stemmer) > 0) {
			    int j;
			    if (inlen < 30) {
				for (j = 30 - inlen; j > 0; j--)
				    fputs(" ", f_out);
			    } else {
				fputs("\n", f_out);
				for (j = 30; j > 0; j--)
				    fputs(" ", f_out);
			    }
			}
		    }

		    fputs((const char *)stemmed, f_out);
		    putc('\n', f_out);
		}
            }
        }
    }
error:
    if (b != 0) free(b);
    return;
}

int main(/*int argc, char * argv[]*/) {
    struct sb_stemmer * stemmer;

    char * language = "czech";
    char * charenc = "UTF_8";

    pretty = 0;
    // progname = argv[0];

    /* do the stemming process: */
    stemmer = sb_stemmer_new(language, charenc);
    if (stemmer == 0) {
        if (charenc == NULL) {
            fprintf(stderr, "language `%s' not available for stemming\n", language);
            exit(1);
        } else {
            fprintf(stderr, "language `%s' not available for stemming in encoding `%s'\n", language, charenc);
            exit(1);
        }
    }
    stem_file(stemmer, stdin, stdout);
    sb_stemmer_delete(stemmer);

    return 0;
}

