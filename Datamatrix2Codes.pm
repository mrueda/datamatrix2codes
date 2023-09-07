package Datamatrix2Codes;

use strict;
use warnings;
use feature qw(say);
use Data::Dumper;
use Text::CSV_XS qw(csv);
use Exporter 'import';

our @EXPORT_OK = ( 'parse_encoded_string', 'load_data_from_file' );

use constant DEVEL_MODE => 0;

sub parse_encoded_string {

    my $encoded_str = shift;
    say $encoded_str if DEVEL_MODE;

    my $data;

    # PC
    $encoded_str =~ m/01[01](8\d{8,}?)(10|17|21|$)/;
    $data->{PC} = $1;
    $encoded_str =~ s/$1//;
    say $encoded_str if DEVEL_MODE;

    # SN
    $encoded_str =~ m/21(\w{8,}?)(10|17|71|$)/;
    $data->{SN} = $1;
    $encoded_str =~ s/$1//;
    say $encoded_str if DEVEL_MODE;

    # LOTE
    $encoded_str =~ m/(?<!^0)10(\w{3,}?)(?=21|17|71|$)/;
    $data->{LOTE} = $1;
    say "<LOTE:$1>" if DEVEL_MODE;
    $data->{LOTE} =~ s/^(10|3110)// if $1;
    $encoded_str  =~ s/$data->{LOTE}//  if $1;
    say $encoded_str if DEVEL_MODE;

    # CAD
    $encoded_str =~ m/17(\d{4})(21|10|30|31|71)/;
    $data->{CAD} = $1;
    say "<CAD:$1>" if DEVEL_MODE;
    say "$encoded_str\n" if DEVEL_MODE;

    return $data;
}

sub load_data_from_file {

    my $filename = shift;
    my %months   = (
        'Jan' => '01',
        'Feb' => '02',
        'Mar' => '03',
        'Apr' => '04',
        'May' => '05',
        'Jun' => '06',
        'Jul' => '07',
        'Aug' => '08',
        'Sep' => '09',
        'Oct' => '10',
        'Nov' => '11',
        'Dec' => '12'
    );

    my $aoh =
      csv( in => $filename, sep_char => "\t", headers => [ 'PC', 'SN', 'LOTE', 'CAD' ] );

    for my $item (@$aoh) {
        my ($month, $year ) = split /\-/, $item->{CAD};
        $item->{CAD} = $year . $months{$month};
    }
    return $aoh;
}

1;
