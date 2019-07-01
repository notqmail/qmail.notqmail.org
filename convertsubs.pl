#!/usr/bin/perl
##  convertsubs.pl v0.99
## 
## Stuart Bain <gun@gunandgiz.com>
## 
## Based on convert-and-create.pl which was
## put into the public domain by Russell Nelson <nelson@qmail.org>
## 
## This program is meant to be used as a followup to Mr. Nelson's
## convert-and-create.pl script. Microsoft Outlook Express uses
## mbox formatted files in the users' home directories to store
## subfolders. This script will search through each user's home
## directory for mbox formatted files. If it finds any, it will convert
## them to Maildir format and place them in the appropriate
## directory for use with the Courier IMAP Daemon
## (http://www.inter7.com/courierimap/). You can find these directories
## as hidden directories underneath the main Maildir.
## 
## For example, if there was an IMAP subdir named "Customers" then
## you will find a mbox formatted file called "Customers" in the user's
## directory. This script will then create ~/Maildir/.Customers/ and
## populate the directory with the messages from the mbox file.
## This script will not delete the mbox file. Once you are certain
## everything looks right, you can manually delete it (or write a script
## to do it for you :P).
## 
## The only drawback to using this script (as well as the
## convert-and-create script) is that the delivery date and time for
## the messages is changed to the conversion time (whenever the
## script ran). In addition, no subdirectories are processed, only
## mbox formatted files in the user's home directory.
##
## Please note that this program creates a log to STDOUT, so you
## may want to redirect it to a file if you want to save a copy of
## what the program converted and what it skipped.
##  
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License (http://www.gnu.org/copyleft/gpl.html)
## for more details.
## 
## Version History:
## -- version 0.01 inital development code
## -- version 0.99 initial release code
##
## Support for this script and Mr. Nelson's convert-and-create script are
## available from their respective authors.
##
## Ni!!!!!!
##
#############################################################################

# Loop through the /etc/passwd file grabbing the users' info
while(($name, $passwd, $uid, $gid, $quota, $comment, $gcos, $dir, $shell) = getpwent()) {
	if (!-e $dir) {
		print "warning: ${name}'s home dir, $dir, doesn't exist (passwd: $passwd), skipping.\n";
		next;
	}
	$st_uid = (stat($dir))[4];;
	if ($uid != $st_uid) {
		print "warning: $name is $uid, but $dir is owned by $st_uid, skipping.\n";
		next;
	}

	$spoolname = "$dir/Maildir";
	print "\n-------------------------------------------------\nNow processing $name.\nMail directory is $spoolname.\n";

	# Obtain a list of the user's files
	opendir HOMEDIR, $dir or die "Unable to open $name home directory:\n$!\n";
	@userfiles = readdir HOMEDIR;
	closedir HOMEDIR;

	# Process each file
	FILEPROC: foreach $filename (@userfiles) {
		$openfile = "$dir/$filename";

		# Skip files that aren't text files
		if (!-T $openfile) {
			print "$openfile is not a Text file, skipping to next file.\n\n";
			next FILEPROC;
		}

		print "Now processing $openfile folder.\n";
               
		open(INPUTFILE, "<$openfile") or die "Unable to open $openfile:\n$!\n";

		$linecount = 0;
		$i = time;

		while (<INPUTFILE>) {
			$linecount++;

			if ($linecount == 1) {

				#New mail file? Create the subdirectories for it
				if (/^From /) {
					print "Creating directories for $filename.\n";
					$newdir = "$spoolname/.$filename";
					if (!-d $newdir) {
						mkdir $newdir,0700 || die "Unable to create directory for $filename:\n$!\n";
						chown ($uid,$gid,$newdir);
						chdir($newdir) || die("Unable to chdir to $spoolname:\n$!\n");
						-d "tmp" || mkdir("tmp",0700) || die("Unable to make tmp/ in $newdir:\n$!\n");
						-d "new" || mkdir("new",0700) || die("Unable to make new/ in $newdir:\n$!\n");
						-d "cur" || mkdir("cur",0700) || die("Unable to make cur/ in $newdir:\n$!\n");
						chown ($uid,$gid,"tmp","new","cur");
					}    
				}

				#If not, we don't care... go to the next file
				else {
					print "$filename doesn't appear to be an mbox formatted mailbox it will be skipped.\n\n";
					next FILEPROC;
				}
			}

			# Now that we have the folders created, start a new file if we encounter a new message in the mbox file
			if (/^From /) {
				$fn = sprintf("new/%d.$$.mbox", $i);
				open(OUT, ">$fn") || die("Unable to create new message:\n$!\n");;
				chown ($uid,$gid,$fn);
				$i++;
				next;
			}

			# Not quite sure what this line is for, but I left it in and everything
			# seems to work fine.
			s/^>From /From /;

			# If we didn't start a new message, print the lines for the header/body of the msg.
			print OUT || die("Unable to write to new message:\n$!\n");                    

		}  
	}

	# Clean up a little before we leave
	close (INPUTFILE);
	close (OUT);

}

endpwent();