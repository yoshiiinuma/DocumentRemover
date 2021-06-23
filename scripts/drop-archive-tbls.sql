
DROP INDEX ArchivedRequests_Status_IX on ArchivedRequests;
DROP INDEX ArchivedRequests_ArchiveDate_IX on ArchivedRequests;

DROP INDEX ArchivedFiles_RequestId_IX on ArchivedFiles;
DROP INDEX ArchivedFiles_FileId_IX on ArchivedFiles;

DROP TABLE ArchivedFiles;
DROP TABLE ArchivedRequests;

