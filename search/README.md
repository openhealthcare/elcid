How to search an how to extract

Searchin uses Search Rules

A search rule is a discoverable feature.

By default all subrecords are wrapped in search rules.

To override a subrecord's search rule, create a search rule with the slug of a subrecords api name.

By default a search rule will allow you to search on all fields.

If you declare a field attribute, only these fields will be used.

If you declare an attribute on the class with a field name, this will be used
instead of the subrecordfield

If you declare additional fields. These will be added.

If you declare a list of field names, then only
these will be searchable.

If a user has the role 'extract_personal_details' they will be able to extract
all data including hospital number/name

TO DO
rename column to row in the query
rename the schema.subrecord to schema.rule
fix the description box
figure out a way where we can choose to sended a nested extract, or not
bring down required fields by declaration in the extract
remove the and or combination in its current state
extract the subrecord discoverable into a subrecord wrapper
extract the fields into fields wrappers
allow loading in of data
order nested extracts, patient, episode then subrecords
