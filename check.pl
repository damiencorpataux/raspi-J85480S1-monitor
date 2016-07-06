#!/usr/bin/perl

############################################################################
##
## check_nagios
##
## Checks the given service for alarms.
##
## This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
## USA
##
## 2016-06-29 Damien Corpataux - initial version
##
############################################################################

use warnings;
use Try::Tiny;
use Getopt::Long;
use LWP::UserAgent;
use HTTP::Request;
use JSON;

no warnings 'experimental::smartmatch';


## CLI handler
sub Usage() {
  printf("\nUsage: %s [PARAMETERS] Parameters:
  --url=[URL] : The URL of the service to call\n\n", $ARGV[0])
}
my $options = {
  'url' => ''
};
GetOptions ($options, "url=s");
foreach (keys %{$options}) {
  if ( $options->{$_} eq '' ) {
    print "\nError: Parameter missing --$_\n";
    Usage();
    exit(1);
  }
}

## Service call
try {
    $url = sprintf('%s?latch', $options->{'url'});
    $ua = LWP::UserAgent->new;
    $request = HTTP::Request->new(GET => $url);
    $response = $ua->request($request);
    $json = JSON::from_json($response->content);
} catch {
    print "UNKNOWN: Could not fetch web-service data ($url)";
    exit 3;
};

## Result processing
try {
    # Make a list of alarms
    my $alarms_all = %$json{alarms};
    my @alarms_discard = ('OK', 'Non-catastrophic Internal Failure');
    my %alarms_active = ();
    while (my ($module, $alarms) = each %$alarms_all) {
        while (my ($key, $value) = each %$alarms) {
             if ($value & !($key ~~ @alarms_discard)) {
                if (!$alarms_active{$module}) {
                    $alarms_active{$module} = [];
                }
                push(@{$alarms_active{$module}}, $key)
            }
        }
    }
    # Create alarms string
    $alarms_strings = [];
    while (my ($module, $alarms) = each %alarms_active) {
        push(@$alarms_strings, "$module: " . join(' -or- ', @$alarms));
    }
    $alarms_string = join('; ', @$alarms_strings);
    # Nagios check output
    if (!$json->{'human'}{'Fault'} &
        !$json->{'human'}{'OTW'} &
        !$json->{'human'}{'PFW_1'} &
        !$json->{'human'}{'PFW_2'} &
        !$json->{'human'}{'PFW_3'} &
        !$json->{'human'}{'PFW_4'} ) {
        print "OK: Everything looks fine";
        exit 0;
    } elsif ( $json->{'human'}{'Fault'} ) {
        print "CRIT: Fault ($alarms_string)";
        exit 2;
    } else {
        print "WARN: $alarms_string";
        exit 1;
    }
} catch {
    print "UNKNOWN: Could not process web-service data ($url)";
    exit 3;
};