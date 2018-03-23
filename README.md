# mantisbt_database_tweaker

This is a command line application that lets you tweak the MantisBT database.

- Bugs
    - Change owner
    - Change date submitted
- Monitor
    - Add monitor to an issue
    - Delete monitor from issue
- Bugnotes
    - Add bugnote
    - Move bugnote
    - Modify time tracking
    - Modify time
    - Modify owner
- Categories
    - Modify category
    - Delete category


## Requirements
Currently only tested using MantisBT 1.2.8 but may work with later versions.
Requires _mysql Python module to be available.

## Installation
1. Download the file and place it in a directory on your `PATH`.
1. Edit and change the MySQL access credientials in the CONFIG section.
1. Save and run!

## Example usage
```
MantisBT Database Tweaker v2.0
==============================

Bugs
----
1) Change owner

Monitor
-------
2) Add monitor to an issue
3) Delete monitor from issue

Bugnotes
--------
4) Add bugnote
5) Move bugnote
6) Modify time tracking
7) Modify time
8) Modify owner

Categories
----------
9) Modify category
10) Delete category

Enter selection (return to exit): 8

=====================
Change bugnote owner
---------------------

  4 Marcel       Wave                 user1
 32 Sid          Snot                 user2
 31 Cupid        Stunt                user3

Select user id:  32
Enter bugnote number:  123
Change owner of 'My email is broken' to 'Sid Snot (32)'
[y/n]: y

Rollback: UPDATE mantis_bugnote_table SET reporter_id = 4 WHERE id = 123
UPDATE mantis_bugnote_table SET reporter_id = 32 WHERE id = 123
```


