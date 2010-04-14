#!/usr/bin/perl -w

use strict;
use CGI qw/:cgi/;
use File::Basename qw/basename/;

my $storage_path = 'data';

my $q = new CGI;
my $path = $q->param('p');
unless( $path && -e "./data/$path" ) {
  print $q->header('text/html', '404 Not Found');
  print "404 Not Found\n";
  exit;
}

unless( -r "./data/$path" ) {
  print $q->header('text/html', '403 Forbidden');
  print "403 Forbidden\n";
  exit;
}

my $fh;
unless( open $fh, '<', "./data/$path" ) {
  print $q->header('text/html', '500 Internal Server Error');
  print "File open failed\n";
  exit;
}

my $size = -s "./data/$path";
#283     header("Content-Type: application/octet-stream");
#284     header("Content-Size: ".filesize($file));
#285     header("Content-Disposition: attachment; filename=\"".basename($file)."\"");
#286     header("Content-Length: ".filesize($file));
#287     header("Content-transfer-encoding: binary");

print $q->header(
  -type => 'application/octet-stream',
  -Content_Size => $size,
  -attachment => basename($path),
  -Content_Length => $size,
  -Content_transfer_encoding => 'binary'
);

my $content;
while( sysread $fh, $content, 4096 ) {
  print $content;
}

close $fh;
exit;
1;
