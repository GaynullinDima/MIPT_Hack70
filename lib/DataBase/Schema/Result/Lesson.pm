use utf8;
package DataBase::Schema::Result::Lesson;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

DataBase::Schema::Result::Lesson

=cut

use strict;
use warnings;

use base 'DBIx::Class::Core';

=head1 TABLE: C<lesson>

=cut

__PACKAGE__->table("lesson");

=head1 ACCESSORS

=head2 lesson_id

  data_type: 'integer'
  is_auto_increment: 1
  is_nullable: 0

=head2 course_id

  data_type: (empty string)
  is_foreign_key: 1
  is_nullable: 1

=head2 day_id

  data_type: (empty string)
  is_foreign_key: 1
  is_nullable: 1

=head2 num

  data_type: 'integer'
  is_nullable: 1

=cut

__PACKAGE__->add_columns(
  "lesson_id",
  { data_type => "integer", is_auto_increment => 1, is_nullable => 0 },
  "course_id",
  { data_type => "", is_foreign_key => 1, is_nullable => 1 },
  "day_id",
  { data_type => "", is_foreign_key => 1, is_nullable => 1 },
  "num",
  { data_type => "integer", is_nullable => 1 },
);

=head1 PRIMARY KEY

=over 4

=item * L</lesson_id>

=back

=cut

__PACKAGE__->set_primary_key("lesson_id");

=head1 RELATIONS

=head2 course

Type: belongs_to

Related object: L<DataBase::Schema::Result::Course>

=cut

__PACKAGE__->belongs_to(
  "course",
  "DataBase::Schema::Result::Course",
  { course_id => "course_id" },
  {
    is_deferrable => 0,
    join_type     => "LEFT",
    on_delete     => "NO ACTION",
    on_update     => "NO ACTION",
  },
);

=head2 day

Type: belongs_to

Related object: L<DataBase::Schema::Result::Day>

=cut

__PACKAGE__->belongs_to(
  "day",
  "DataBase::Schema::Result::Day",
  { day_id => "day_id" },
  {
    is_deferrable => 0,
    join_type     => "LEFT",
    on_delete     => "NO ACTION",
    on_update     => "NO ACTION",
  },
);

=head2 ratings

Type: has_many

Related object: L<DataBase::Schema::Result::Rating>

=cut

__PACKAGE__->has_many(
  "ratings",
  "DataBase::Schema::Result::Rating",
  { "foreign.lesson_id" => "self.lesson_id" },
  { cascade_copy => 0, cascade_delete => 0 },
);

=head2 schedules

Type: has_many

Related object: L<DataBase::Schema::Result::Schedule>

=cut

__PACKAGE__->has_many(
  "schedules",
  "DataBase::Schema::Result::Schedule",
  { "foreign.lesson_id" => "self.lesson_id" },
  { cascade_copy => 0, cascade_delete => 0 },
);


# Created by DBIx::Class::Schema::Loader v0.07039 @ 2016-11-20 03:20:46
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:l/7ybNtV+iX4cB3OQo3JvQ


# You can replace this text with custom code or comments, and it will be preserved on regeneration
1;
