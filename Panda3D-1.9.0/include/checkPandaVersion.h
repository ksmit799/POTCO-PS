
# include "dtoolbase.h"
extern EXPCL_DTOOL int panda_version_1_9;
# ifndef WIN32
/* For Windows, exporting the symbol from the DLL is sufficient; the
      DLL will not load unless all expected public symbols are defined.
      Other systems may not mind if the symbol is absent unless we
      explictly write code that references it. */
static int check_panda_version = panda_version_1_9;
# endif
