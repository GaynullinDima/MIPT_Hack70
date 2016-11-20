package ExcelParser::Parser;

use strict;
use warnings;
use Spreadsheet::Read;
use Spreadsheet::ParseExcel;
use enum qw(Mon Tue Wed Thu Fri Sat);
use DDP;
use Mouse;
use Encode qw(encode decode is_utf8);
use 5.010;


has file_name => (
	is  => 'ro',
	isa => 'Str',
	required => 1
);

has rows => (
	is => 'ro',
	isa => 'ArrayRef',
	builder => '_build_rows' 
);

has book => (
	is  => 'rw',
	isa => 'Any'
);

has initial_row => (
	is => 'ro',
	isa => 'Int',
	default => 4
);

has initial_col => (
	is => 'ro',
	isa => 'Int',
	default => 5
);

sub _build_rows {
	my $self = shift;

	my $book = ReadData($self->file_name, attr => 1, merged => 1);
	$self->book($book);
	

	my @rows = Spreadsheet::Read::rows($book->[1]);

	return \@rows;
}

sub parse_table {
	my $self = shift;

	my %table;

	for my $row_pos( 0 .. $#{ $self->rows->[$self->initial_row] } ) {
		my $cell = $self->rows->[$self->initial_row]->[$row_pos];
		if ( $cell and $cell =~ /^\d+$/ ) {
			$table{$cell} = $self->_parse_group_column($row_pos)	
		}
	}

	return \%table;
}

sub _parse_group_column {
	my ($self, $row_pos) = @_;
	
	my @days;
	my $col_pos = $self->initial_col;
	for my $day (Mon .. Sat) {
		push @days, $self->_parse_day($row_pos, \$col_pos);
	}

	return \@days;
}

sub _parse_day {
	my ($self, $row_pos, $col_pos) = @_;
	
	my @lessons;

	my @row_nums;

	while (1) {
		next unless $self->rows->[$$col_pos]->[1];
		push @row_nums, [$row_pos, $$col_pos];	
		last if $self->rows->[$$col_pos]->[1] =~ /19/;
	}
	continue {
		$$col_pos++;
	}

	for my $cell (@row_nums) {
		push @lessons, $self->_parse_lesson(@$cell);
	}
	
	$$col_pos++;		
	return \@lessons;				
}

sub _parse_lesson {
	my ($self, $row_pos, $col_pos) = @_;

	my @lesson;
	my $cell_pos = cr2cell($row_pos + 1, $col_pos + 1);
	my $cell = $self->book->[1]{$cell_pos} || return undef;

	#p $self->book->[1]->{attr}[$row_pos + 1][$col_pos + 1]{merged};

	if ( $cell =~ /(.+)\/.*\//) {
		push @lesson, $1;        # [0] : name
		push @lesson, "lecture"; # [1] : type
	}
	else {
		push @lesson, $cell;
		push @lesson, "seminar";
	}
	
	return \@lesson;
}

1;
