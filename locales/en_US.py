#!/usr/bin/python
# -*- coding: utf-8 -*-

MESSAGES = {
	"READING_FILE": "Reading %s...",
	"READING_STRINGBLOCK": "Reading stringblock from %s...",
	"TOTAL_ROWS": "%i rows total",
	"USING_GENERATED_STRUCTURE": "Using generated structure for file %s, build %i",
	"USING_STRUCTURE": "Using %s structure build %i",
	"WRITTEN_BYTES": "Written %i bytes at %s",
	
	"BUILD_NOT_SET": "Build not set for a DBC file; assuming default structure.",
	"COLUMN_NOT_FOUND": "Column %r not found",
	"FILENAME_NOT_SPECIFIED": "wdbc.new requires a 'name' argument to function correctly",
	"FILETYPE_NOT_WRITABLE": "%s is not a writable filetype",
	"MULTIPLE_ROW_INSTANCE": "Multiple instances of row #%i found",
	"STRUCTURE_NOT_FOUND": "Structure not found for file %r",
	"PATH_NOT_SET": "DBFile.path needs to be set before initiating parsing",
	"PATH_NOT_VALID": "DBFile.path needs to be a valid file before initiating parsing",
	"DIFFERENT_ROW_COUNT": "Read %i rows, expected %i.",
	"DBC_RECLEN_NOT_RESPECTED": "File structure does not respect DBC reclen. Expected %i, reading %i. (%+i)",
	"DBC_INCORRECT_FIELD_COUNT": "File structure does not respect DBC field count. Expected %i, got %i instead.",
	"RECLEN_NOT_RESPECTED": "Reclen not respected for row %i. Expected %i, read %i. (%+i)",
	"NOT_A_WDB_FILE": "%r is not a valid WDB or DBC file: %r",
	"SUBSTRING_NOT_FOUND": "No string was found at address %i. This is most often caused by a bad structure. Doublecheck your StringFields!",
}
