====================
The report.yaml File
====================

What is YAML?::

    YAML is a human-readable data serialization format that takes concepts from programming languages
    such as C, Perl, and Python, and ideas from XML and the data format of electronic mail. It also rhymes with "camel".

How do I use the report.yaml file?::

    The report.yaml file is used to quickly configure simple reports without having to write the python to have
    Django access the database. Take this for an example:

    FooTable: # table specifier
      column1: null # column specifier
      column2: null
      column3: null

    This will load the three columns specified for all records in FooTable as a list of of lists.

    The column specifier consists of two parts. The name of the column and an operation or value. Let's assume
    you have a table where you wish to filter on a column called customer_id:

    FooTable:
      customer_id: 12
      date: null
      item: null
      name: null

    This will load the two columns date and item for all records in FooTable where customer_id is 12.

You can also have an operation as the value::

    FooTable:
      customer_id: CustomerTable.customer_id:customer_email=customer@localhost.xxx
      date: null
      item: null
      name: null

    This will load the data as above by looking up the customer_id in the CustomerTable where the customer_email matches
    the specified value.

Django also provides a number of filtering operators which can be used

**exact**
::

    FooTable:
      customer_id: exact 12 # NOTE: This is identical to customer_id: 12
      date: null
      item: null
      name: null

**iexact**
::

    FooTable:
      customer_id: null
      date: null
      item: null
      name: iexact coffee maker # Case insensitive SQL: SELECT ... WHERE name ILIKE 'coffee maker';

**contains**
::

    FooTable:
      customer_id: null
      date: null
      item: null
      name: contains ee ma # SQL: SELECT ... WHERE name LIKE '%ee ma%';

**in**
::

    FooTable:
      customer_id: null
      date: null
      item: in [1, 12, 14, 'a'] # SQL: SELECT ... WHERE item IN (1, 12, 14, 'a');
      name: null

**gt**
::

    FooTable:
      customer_id: gt 12 # SQL: SELECT ... WHERE customer_id > 12
      date: null
      item: null
      name: null

**gte**
::

    FooTable:
      customer_id: gte 12 # SQL: SELECT ... WHERE customer_id >= 12
      date: null
      item: null
      name: null

**lt**
::

    FooTable:
      customer_id: lt 12 # SQL: SELECT ... WHERE customer_id < 12
      date: null
      item: null
      name: null

**lte**
::

    FooTable:
      customer_id: lte 12 # SQL: SELECT ... WHERE customer_id <= 12
      date: null
      item: null
      name: null

**startswith**
::

    FooTable:
      customer_id: null
      date: null
      item: null
      name: startswith Coff # SQL: SELECT ... WHERE name LIKE 'Coff%';

**istartswith**
::

    FooTable:
      customer_id: null
      date: null
      item: null
      name: istartswith coff # SQL: SELECT ... WHERE name ILIKE 'coff%';

**endswith**
::

    FooTable:
      customer_id: null
      date: null
      item: null
      name: endswith maker # SQL: SELECT ... WHERE name LIKE '%maker';

**iendswith**
 ::

    FooTable:
      customer_id: null
      date: null
      item: null
      name: iendswith maker # SQL: SELECT ... WHERE name ILIKE '%maker';

**range**
 ::

    FooTable:
      customer_id: range 2, 25 # SQL: SELECT ... WHERE customer_id BETWEEN 2 and 25;
      date: null
      item: null
      name: null

**isnull**
 ::

    FooTable:
      customer_id: null
      date: null
      item: isnull True | False # SQL: SELECT ... WHERE item IS NULL;
      name: null

**regex**
 ::

    FooTable:
      customer_id: null
      date: null
      item: null
      name: regex (^Cof.*) # SQL: SELECT ... WHERE title REGEXP BINARY '(^Cof.*)';
      # NOTE: Under the hood different database implementations might have some
      # implementation specific regular expression considerations

**iregex**
 ::

    FooTable:
      customer_id: null
      date: null
      item: null
      name: iregex (^cof.*) # SQL: SELECT ... WHERE title REGEXP BINARY '(^cof.*)';
      # NOTE: Under the hood different database implementations might have some
      # implementation specific regular expression considerations

**search**
 ::

    FooTable:
      customer_id: null
      date: null
      item: /null
      name: null
      notes: search +Coffee -creamer Electric +grinder
      # NOTE: not implemented for demo

*Dates are special.*

**date_range**
::

    FooTable:
      customer_id: CustomerTable.customer_id:customer_email=customer@localhost.xxx
      date: date_range 2005-01-01, 2005-03-31 # SQL: SELECT ... WHERE date BETWEEN '2005-01-01' and '2005-03-31';
      item: null
      name: null
      #NOTE: date_range is not actually implemented for the demo.

**year**
::

    FooTable:
      customer_id: CustomerTable.customer_id:customer_email=customer@localhost.xxx
      date: year 2005 # SQL: SELECT ... WHERE date BETWEEN '2005-01-01' and '2005-03-31';
      item: null
      name: null

**month**
::

    FooTable:
      customer_id: CustomerTable.customer_id:customer_email=customer@localhost.xxx
      date: month 12 # SQL: SELECT ... WHERE EXTRACT('month' from date) = '12';
      item: null
      name: null

**day**
::

    FooTable:
      customer_id: CustomerTable.customer_id:customer_email=customer@localhost.xxx
      date: day 12 # SQL: SELECT ... WHERE EXTRACT('day' from date) = '12';
      item: null
      name: null

**week_day**
::

    FooTable:
      customer_id: CustomerTable.customer_id:customer_email=customer@localhost.xxx
      date: week_day 1 # No sql equivalent. Take an integer 1 (Sunday) - 7 (Saturday)
      item: null
      name: null

**hour**
::

    FooTable:
      customer_id: CustomerTable.customer_id:customer_email=customer@localhost.xxx
      date: hour 12 SQL: SELECT ... WHERE EXTRACT('hour' from date) = '12';
      item: null
      name: null

**minute**
::

    FooTable:
      customer_id: CustomerTable.customer_id:customer_email=customer@localhost.xxx
      date: minute 12 SQL: SELECT ... WHERE EXTRACT('minute' from date) = '12';
      item: null
      name: null

**second**
::

    FooTable:
      customer_id: CustomerTable.customer_id:customer_email=customer@localhost.xxx
      date: second 12 SQL: SELECT ... WHERE EXTRACT('second' from date) = '12';
      item: null
      name: null

