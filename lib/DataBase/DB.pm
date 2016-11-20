package DataBase::DB;

use strict;
use warnings;
use DataBase::Schema;

my $db;
my $db_file = '/home/gregory228/hack/MIPT_Hack70/data_base.db';

sub db {
	$db ||= DataBase::Schema->connect('dbi:SQLite:' . $db_file);
}

1;
