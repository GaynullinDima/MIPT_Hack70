use utf8;
package DataBase::Schema::Result::Course;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

DataBase::Schema::Result::Course

=cut

use strict;
use warnings;

use base 'DBIx::Class::Core';

=head1 TABLE: C<course>

=cut

__PACKAGE__->table("course");

=head1 ACCESSORS

=head2 course_id

  data_type: 'integer'
  is_auto_increment: 1
  is_nullable: 0

=head2 course_type_id

  data_type: (empty string)
  is_foreign_key: 1
  is_nullable: 1

=head2 course_name

  data_type: 'varchar'
  is_nullable: 1
  size: 255

=cut

__PACKAGE__->add_columns(
  "course_id",
  { data_type => "integer", is_auto_increment => 1, is_nullable => 0 },
  "course_type_id",
  { data_type => "", is_foreign_key => 1, is_nullable => 1 },
  "course_name",
  { data_type => "varchar", is_nullable => 1, size => 255 },
);

=head1 PRIMARY KEY

=over 4

=item * L</course_id>

=back

=cut

__PACKAGE__->set_primary_key("course_id");

=head1 RELATIONS

=head2 course_type

Type: belongs_to

Related object: L<DataBase::Schema::Result::CourseType>

=cut

__PACKAGE__->belongs_to(
  "course_type",
  "DataBase::Schema::Result::CourseType",
  { course_type_id => "course_type_id" },
  {
    is_deferrable => 0,
    join_type     => "LEFT",
    on_delete     => "NO ACTION",
    on_update     => "NO ACTION",
  },
);

=head2 lessons

Type: has_many

Related object: L<DataBase::Schema::Result::Lesson>

=cut

__PACKAGE__->has_many(
  "lessons",
  "DataBase::Schema::Result::Lesson",
  { "foreign.course_id" => "self.course_id" },
  { cascade_copy => 0, cascade_delete => 0 },
);


# Created by DBIx::Class::Schema::Loader v0.07039 @ 2016-11-20 03:20:46
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:WvvmTAABKvFKDTDglAOpAA


# You can replace this text with custom code or comments, and it will be preserved on regeneration
1;
