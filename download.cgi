#!/usr/bin/perl -w

use strict;
use CGI qw/:cgi/;
use File::Basename qw/basename/;

my $storage_path = 'data';

my $q = new CGI;
my $path = $q->param('p');
$path =~ s,\.\./,,g;
$path = "./$storage_path/$path";
$path =~ s,//,/,g;
unless( $path && -e $path ) {
  print $q->header('text/html', '404 Not Found');
  print "404 Not Found\n";
  exit;
}

unless( -r $path ) {
  print $q->header('text/html', '403 Forbidden');
  print "403 Forbidden\n";
  exit;
}

my $fh;
unless( open $fh, '<', $path ) {
  print $q->header('text/html', '500 Internal Server Error');
  print "File open failed\n";
  exit;
}

my $size = -s $path;
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
