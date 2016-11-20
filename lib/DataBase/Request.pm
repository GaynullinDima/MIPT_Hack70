package DataBase::Request;

use strict;
use warnings;
use 5.010;

use DataBase::DB;
use Mouse;
use enum qw(Mon Tue Wed Thu Fri Sat);
use enum qw(Name Type);

use DDP;

has db => (
	is => 'ro',
	isa => 'Any',
	default => sub {
		DataBase::DB->db;
	}
);

has request => (
	is => 'ro',
	isa => 'HashRef',
	required => 1,
	trigger => sub {
		my $self = shift;

		$self->_request_handler;
	}
);


sub _request_handler {
	my $self = shift;
	
	#$self->db->storage->debug(1);	

	for my $group ( keys %{$self->request} ) {
		my $group_table = $self->request->{$group};
		for my $day (Mon .. Sat) {
			next unless defined $group_table->[$day];
			for my $lesson ( 0 .. $#{ $group_table->[$day] } ) {
				next unless defined $group_table->[$day]->[$lesson];
				eval {
					my $course_type_name = $group_table->[$day]->[$lesson]->[Type];
					my $course_type = $self->db->resultset('CourseType')
									  ->find({course_type_name => $course_type_name});
					#p $course_type->course_type_id;
					my $course = $self->db->resultset('Course')->find_or_create({
						course_name => $group_table->[$day]->[$lesson]->[Name],
						course_type_id => $course_type->id
					});

					my $lesson_rs = $self->db->resultset('Lesson')->create({
						num => $lesson,
						course_id=> $course->id,
						day_id => $day + 1
					});
					
					$self->db->resultset('Schedule')->create({
						group_id => $group,
						lesson_id => $lesson_rs->id						
					});

				1} or die "Creature failed!";
			}
		}
	}	
}

1;
