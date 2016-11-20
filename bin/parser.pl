#!/usr/perl/bin

use strict;
use warnings;

use FindBin;
use lib "$FindBin::Bin/../lib";

use ExcelParser::Parser;
use DataBase::Request;
use DDP;
use 5.010;

my $parser = ExcelParser::Parser->new(
	file_name => '3-kurs-osen-2016.xls'
);

my $href = $parser->parse_table();


my $request = DataBase::Request->new(
	request => $href
);
