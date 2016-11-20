use utf8;
package DataBase::Schema::Result::Day;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

DataBase::Schema::Result::Day

=cut

use strict;
use warnings;

use base 'DBIx::Class::Core';

=head1 TABLE: C<day>

=cut

__PACKAGE__->table("day");

=head1 ACCESSORS

=head2 day_id

  data_type: 'integer'
  is_auto_increment: 1
  is_nullable: 0

=head2 day_name

  data_type: 'varchar'
  is_nullable: 1
  size: 15

=cut

__PACKAGE__->add_columns(
  "day_id",
  { data_type => "integer", is_auto_increment => 1, is_nullable => 0 },
  "day_name",
  { data_type => "varchar", is_nullable => 1, size => 15 },
);

=head1 PRIMARY KEY

=over 4

=item * L</day_id>

=back

=cut

__PACKAGE__->set_primary_key("day_id");

=head1 RELATIONS

=head2 lessons

Type: has_many

Related object: L<DataBase::Schema::Result::Lesson>

=cut

__PACKAGE__->has_many(
  "lessons",
  "DataBase::Schema::Result::Lesson",
  { "foreign.day_id" => "self.day_id" },
  { cascade_copy => 0, cascade_delete => 0 },
);


# Created by DBIx::Class::Schema::Loader v0.07039 @ 2016-11-20 03:20:46
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:WRhlW+X9yCczonLKz+VFPg


# You can replace this text with custom code or comments, and it will be preserved on regeneration
1;
