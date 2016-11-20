use utf8;
package DataBase::Schema::Result::CourseType;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

DataBase::Schema::Result::CourseType

=cut

use strict;
use warnings;

use base 'DBIx::Class::Core';

=head1 TABLE: C<course_type>

=cut

__PACKAGE__->table("course_type");

=head1 ACCESSORS

=head2 course_type_id

  data_type: 'integer'
  is_auto_increment: 1
  is_nullable: 0

=head2 course_type_name

  data_type: 'varchar'
  is_nullable: 1
  size: 15

=cut

__PACKAGE__->add_columns(
  "course_type_id",
  { data_type => "integer", is_auto_increment => 1, is_nullable => 0 },
  "course_type_name",
  { data_type => "varchar", is_nullable => 1, size => 15 },
);

=head1 PRIMARY KEY

=over 4

=item * L</course_type_id>

=back

=cut

__PACKAGE__->set_primary_key("course_type_id");

=head1 RELATIONS

=head2 courses

Type: has_many

Related object: L<DataBase::Schema::Result::Course>

=cut

__PACKAGE__->has_many(
  "courses",
  "DataBase::Schema::Result::Course",
  { "foreign.course_type_id" => "self.course_type_id" },
  { cascade_copy => 0, cascade_delete => 0 },
);


# Created by DBIx::Class::Schema::Loader v0.07039 @ 2016-11-20 03:20:46
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:X/OWhj4lHz3yrk3R/H6srQ


# You can replace this text with custom code or comments, and it will be preserved on regeneration
1;
