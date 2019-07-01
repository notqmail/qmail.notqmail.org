#!/usr/bin/perl

# checkpassword.pl
# 
# Larry M. Smith <chains-chkpass@FahQ2.com>
#

#  
# Expects tcpserver environmental variables $TCPLOCALPORT and $TCPREMOTEIP.  
# See http://cr.yp.to/ucspi-tcp/environment.html
#
# Provided AS IS and free... It works on my system, your's *MAY* be 
# different!!!  YOU as sysadmin, are expected to TEST everything that 
# you bring online!!!  Also, you may not like the way I log failed 
# passwords.
#
# If you see something that could/should be done differently please let me 
# know.
#

#
# You will need these modules installed on your system.
# Please read the respective man pages.
#
use strict qw( vars );
use User::pwent;
use Unix::Syslog qw(:macros);
use Unix::Syslog qw(:subs);


#
# Change these to match your system/site polices.
#
my $MINUID = 500;     # We don't want brute force attacks against root, etc.
my $EGID = "100 100"; # Don't pass extra groups like wheel, etc.
my $RGID = 100;       

$|=1;

my $ipaddr = $ENV{'TCPREMOTEIP'};
my $port = $ENV{'TCPLOCALPORT'};
%ENV=();

my($len,$buf);
open (USER, "<&=3") or exit (-3);
$len = read(USER, $buf, 512);
close USER;
exit(-3) if $len < 4;

my($user, $pass) = split /\x00/, $buf;
$user = lc $user;
$buf = "\x00" x $len;

my $pw = getpwnam($user) || err_unknown();

my $uid   = $pw->uid;
my $phash = $pw->passwd;
my $home  = $pw->dir;
my $shell = $pw->shell;

if ($uid < $MINUID) {
   err_minuid();
   }

if (crypt($pass, $phash) ne $phash) {
   err_badpass();
   }


$ENV{USER}=$user;
$ENV{UID}=$uid+0;
$ENV{HOME}=$home;
$ENV{SHELL}=$shell;

exit(-4) unless $ENV{UID};
chdir $ENV{HOME};
$) = $EGID;
$( = $RGID;
$> = $ENV{UID};
$< = $ENV{UID};
log_pop3();
exec @ARGV;

sub err_unknown {
   openlog("checkpassword.pl: ", LOG_PID, LOG_MAIL);
   syslog(LOG_INFO, "Attempt to login port %d with unknown user (%s) from [%s]", $port, $user, $ipaddr);
   closelog;
   exit(-3);
   }

sub err_minuid{
   openlog("checkpassword.pl: ", LOG_PID, LOG_MAIL);
   syslog(LOG_INFO, "Attempt to login port %d with UID lt %d (%s) from [%s]",$port, $MINUID, $user, $ipaddr);
   closelog;
   exit(-3);
   }

sub err_badpass{
   openlog("checkpassword.pl: ", LOG_PID, LOG_MAIL);
   syslog(LOG_INFO, "Attempt to login port %d failed for UID %d (%s - %s) from [%s] ",$port, $uid, $user, $pass, $ipaddr);
   closelog();
   exit(-3);
   }

sub log_pop3{
   openlog("checkpassword.pl: ", LOG_PID, LOG_MAIL);
   syslog(LOG_INFO, "port %d login successful UID %d (%s) from [%s]",$port, $uid, $user, $ipaddr);
   closelog();
   }

sleep(10);
exit(-4);
