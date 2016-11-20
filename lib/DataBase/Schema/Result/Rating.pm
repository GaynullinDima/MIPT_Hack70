use utf8;
package DataBase::Schema::Result::Rating;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

DataBase::Schema::Result::Rating

=cut

use strict;
use warnings;

use base 'DBIx::Class::Core';

=head1 TABLE: C<rating>

=cut

__PACKAGE__->table("rating");

=head1 ACCESSORS

=head2 rating_id

  data_type: 'integer'
  is_auto_increment: 1
  is_nullable: 0

=head2 lesson_id

  data_type: (empty string)
  is_foreign_key: 1
  is_nullable: 1

=head2 id

  data_type: (empty string)
  is_foreign_key: 1
  is_nullable: 1

=head2 rate

  data_type: 'integer'
  is_nullable: 1

=cut

__PACKAGE__->add_columns(
  "rating_id",
  { data_type => "integer", is_auto_increment => 1, is_nullable => 0 },
  "lesson_id",
  { data_type => "", is_foreign_key => 1, is_nullable => 1 },
  "id",
  { data_type => "", is_foreign_key => 1, is_nullable => 1 },
  "rate",
  { data_type => "integer", is_nullable => 1 },
);

=head1 PRIMARY KEY

=over 4

=item * L</rating_id>

=back

=cut

__PACKAGE__->set_primary_key("rating_id");

=head1 RELATIONS

=head2 id

Type: belongs_to

Related object: L<DataBase::Schema::Result::User>

=cut

__PACKAGE__->belongs_to(
  "id",
  "DataBase::Schema::Result::User",
  { id => "id" },
  {
    is_deferrable => 0,
    join_type     => "LEFT",
    on_delete     => "NO ACTION",
    on_update     => "NO ACTION",
  },
);

=head2 lesson

Type: belongs_to

Related object: L<DataBase::Schema::Result::Lesson>

=cut

__PACKAGE__->belongs_to(
  "lesson",
  "DataBase::Schema::Result::Lesson",
  { lesson_id => "lesson_id" },
  {
    is_deferrable => 0,
    join_type     => "LEFT",
    on_delete     => "NO ACTION",
    on_update     => "NO ACTION",
  },
);


# Created by DBIx::Class::Schema::Loader v0.07039 @ 2016-11-20 12:27:26
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:/IjCc7gUK/b69ZQ8dFbsvg


# You can replace this text with custom code or comments, and it will be preserved on regeneration
1;
