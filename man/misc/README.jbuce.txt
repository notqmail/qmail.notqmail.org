I have modified Jonathan Bradshaw's anti-UCE patches for qmail to work
with qmail 1.02.  The original email describing the patches is below.
The same conditions apply: freely distributable, but if anything breaks,
you keep both halves.

Share and enjoy,
Andrew Pam <xanni@xanadu.net>
Thursday 4 June 1998

----------

From: Jonathan@NrgUp.Com
Subject: My UCE patches for QMAIL 1.01 (Rev C)
Date: Monday June 05, 1998

These patches are a combination of the existing patches:

		dns.patch2 (allow variable length DNS respnses > 512 bytes)
		dns.patch (make Qmail check MAIL FROM domains via DNS check)
		qmail-1.01-rbl.diffs  (Use RBL for spam blocking)
		qmail-antispam4.diff (More antispam patches)
		wildmat-0.2.patch (Allow badmailpattern matching)

And my own changes, updates and ideas. A couple of which are:

   o Changed file buffer from 64 bytes to 10240 (for large badmailfrom)
   o Mail refusal happens at RCPT TO: to allow mail sent to
	POSTMASTER or ABUSE mailboxes to get through (RBL and BMF),
        also provides for better information in syslog.
   o Message to contact postmaster as part of err_bmf()

This patch is freely distributable. However, by implementing it you agree
that if it breaks ANYTHING, you get to keep both halves. I am NOT responsible
for your use of this patch. Test it on a non-production system FIRST etc.

Many thanks to the authors of the above listed patches for their work and
to Dan for the great QMAIL product (http://www.qmail.org/)

For an example badmailfrom file, check you can check out:

	ftp://garbo.nrgup.com/pub/badmailfrom
	ftp://garbo.nrgup.com/pub/badmailpatterns

Changes in rev B:

	o Allow double bounce messages
	o Make error messages to client and syslog more descriptive

Example script I use to call qmail-smtpd from inetd (via tcp-env). It allows
me final control over RBL and relaying.

#!/bin/sh
# in.smtpd (should be run from /var/qmail/bin/tcp-env)

# Check for hosts we allow to relay through us
case "$TCPREMOTEHOST" in
  *.nrgup.com) RELAYCLIENT=;;
esac

# Check for RBL exceptions
case "$TCPREMOTEHOST" in
  *.ix.netcom.com) unset BOUNCEMAIL;;
esac

# Emergency switch for blackhole
#unset BOUNCEMAIL

# Export variables
export RELAYCLIENT
export BOUNCEMAIL

# Run SMTP process
exec /var/qmail/bin/qmail-smtpd
# End of in.smtpd

