use utf8;
package DataBase::Schema::Result::User;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

DataBase::Schema::Result::User

=cut

use strict;
use warnings;

use base 'DBIx::Class::Core';

=head1 TABLE: C<user>

=cut

__PACKAGE__->table("user");

=head1 ACCESSORS

=head2 user_id

  data_type: 'integer'
  is_auto_increment: 1
  is_nullable: 0

=head2 first_name

  data_type: 'varchar'
  is_nullable: 1
  size: 255

=head2 last_name

  data_type: 'varchar'
  is_nullable: 1
  size: 255

=head2 group_id

  data_type: 'integer'
  is_nullable: 1

=cut

__PACKAGE__->add_columns(
  "user_id",
  { data_type => "integer", is_auto_increment => 1, is_nullable => 0 },
  "first_name",
  { data_type => "varchar", is_nullable => 1, size => 255 },
  "last_name",
  { data_type => "varchar", is_nullable => 1, size => 255 },
  "group_id",
  { data_type => "integer", is_nullable => 1 },
);

=head1 PRIMARY KEY

=over 4

=item * L</user_id>

=back

=cut

__PACKAGE__->set_primary_key("user_id");

=head1 RELATIONS

=head2 ratings

Type: has_many

Related object: L<DataBase::Schema::Result::Rating>

=cut

__PACKAGE__->has_many(
  "ratings",
  "DataBase::Schema::Result::Rating",
  { "foreign.user_id" => "self.user_id" },
  { cascade_copy => 0, cascade_delete => 0 },
);

=head2 schedules

Type: has_many

Related object: L<DataBase::Schema::Result::Schedule>

=cut

__PACKAGE__->has_many(
  "schedules",
  "DataBase::Schema::Result::Schedule",
  { "foreign.group_id" => "self.group_id" },
  { cascade_copy => 0, cascade_delete => 0 },
);


# Created by DBIx::Class::Schema::Loader v0.07039 @ 2016-11-20 03:20:46
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:/yED2fuwQei6/MUnV11wOQ


# You can replace this text with custom code or comments, and it will be preserved on regeneration
1;
