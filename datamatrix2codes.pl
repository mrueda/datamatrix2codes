#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;
use feature qw(say);
use lib "./";
use Text::CSV_XS qw(csv);
use Datamatrix2Codes    qw(parse_encoded_string load_data_from_file);

# Ensure a filename is provided
unless ( $ARGV[0] ) {
    die "Usage: $0 <path_to_csv_file> <output.csv>\n";
}

# Read the CSV file using the first argument as the filename
my $filename = $ARGV[0];
open my $fh, '<', $filename or die "Cannot open file: $!";
my $decoded_data;
while ( my $line = <$fh> ) {
    chomp $line;    # Remove newline character
    my $data = parse_encoded_string($line);
    $data->{CODE} = $line;
    push @$decoded_data, $data;
}
close $fh;

# Read the results file (TSV)
my $reference_data = load_data_from_file('data/results.tsv');

#print Dumper $decoded_data;
csv(
    in      => $decoded_data,
    out     => $ARGV[1] // "output.csv",
    headers => [ 'CODE', 'PC', 'SN', 'LOTE', 'CAD' ]
);

#############
# TEST ONLY #
#############
#test_only();

sub test_only {
    for ( my $i = 0 ; $i < @$decoded_data ; $i++ ) {
        for my $id (qw/PC SN LOTE CAD/) {
            next if $reference_data->[$i]{$id} eq '';
            say
"$decoded_data->[$i]{CODE}\n$id PROGRAM: <$decoded_data->[$i]{$id}> - TRUE: <$reference_data->[$i]{$id}> DON'T MATCH!"
              and print "\n"
              unless $decoded_data->[$i]{$id} eq $reference_data->[$i]{$id};
        }
    }
}

