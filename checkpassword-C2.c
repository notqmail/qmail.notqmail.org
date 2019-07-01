/* ----------------------------
   This program requires

  -lsecurity -ldb -laud -lm
 
  libraries to work

You should rename checkpassword-C2.c on checkpassword.c and compile it with
checkpassword-0.90 files.
 
------------------------------ */

#include "error.h"
#include "pathexec.h"
#include "prot.h"

extern char *dispcrypt();

#include </usr/include/pwd.h>
static struct passwd *pw;

#include </usr/sys/include/sys/types.h>
#include </usr/sys/include/sys/security.h>
#include </usr/include/prot.h>
#include </usr/include/crypt.h>
static struct es_passwd *es_pw;

static char up[513];
static int uplen;


main(int argc,char **argv)
{
  char *login;
  char *password;
  char *encrypted;
  char *uxpass;
  int  r;
  int  i;
  int  argc1;
  char *argv1;
  uchar_t crypt_alg;

  (void) set_auth_parameters(argc1, argv1);

  if (!argv[1]) _exit(2);
 
  uplen = 0;
  for (;;) {
    do
      r = read(3,up + uplen,sizeof(up) - uplen);
    while ((r == -1) && (errno == error_intr));
    if (r == -1) _exit(111);
    if (r == 0) break;
    uplen += r;
    if (uplen >= sizeof(up)) _exit(1);
  }
  close(3);

  i = 0;
  if (i >= uplen) _exit(2);
  login = up + i;
  while (up[i++]) if (i >= uplen) _exit(2);
  password = up + i;
  if (i >= uplen) _exit(2);
  while (up[i++]) if (i >= uplen) _exit(2);

  pw = getpwnam(login);
  if (pw)
    uxpass = pw->pw_passwd;
  else {
    if (errno == error_txtbsy) _exit(111);
    _exit(1);
  }

 setprpwent();
 es_pw = getespwnam(login);

 if (es_pw)
 {
   uxpass = es_pw->ufld->fd_encrypt;
   crypt_alg = es_pw->ufld->fd_oldcrypt;
 }
 else
   if (errno == error_txtbsy) _exit(111);

 if (!uxpass) _exit(1);

 encrypted = dispcrypt(password,uxpass,crypt_alg);
 for (i = 0;i < sizeof(up);++i) up[i] = 0;
  
 r = 0;
 if (!*uxpass || strcmp(encrypted,uxpass)) r = 1;
 if (prot_gid((int) pw->pw_gid) == -1) r = 1;
 if (prot_uid((int) pw->pw_uid) == -1) r = 1;
 if (r == 1)
 {
   endprpwent();
   _exit(1);
 }      

 r = 0;
 if (chdir(pw->pw_dir) == -1) r = 1;

 if (!pathexec_env("USER",pw->pw_name)) r = 1;
 if (!pathexec_env("HOME",pw->pw_dir)) r = 1;
 if (!pathexec_env("SHELL",pw->pw_shell)) r = 1;
 if (r == 1)
 {
   endprpwent();
   _exit(1);
 }

 pathexec(argv + 1);
 endprpwent();
//  _exit(111);
}
